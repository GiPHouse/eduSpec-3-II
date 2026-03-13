let jsmeApplet = null;
let isInitialized = false;
let currentWidth = 500;
let currentHeight = 400;

// communication Python (Streamlit) -> JS (JSME component) happens via the Streamlit.RENDER_EVENT
// data communication JS (JSME component)-> Python (Streamlit) happens via Streamlit.setComponentValue() which sends a message up

// Initialize JSME with specified dimensions
function initializeJSME(defaultSmiles = "", width = 500, height = 400, options = "oldlook,star") {
    try {
        // store current dimensions
        currentWidth = width;
        currentHeight = height;

        // destroy an existing JSME instance if exists
        if (jsmeApplet) {
            try {
                jsmeApplet.destroy();
            } catch (e) {
                console.log("Could not destroy previous JSME instance:", e);
            }
            jsmeApplet = null;
        }

        // clear the container with id="jsme" completely before a new instance of the editor is created
        const jsmeContainer = document.getElementById("jsme");
        jsmeContainer.innerHTML = "";

        // wait a bit before creating new instance to ensure cleanup
        setTimeout(() => {
            // create JSME applet with specified dimensions
            jsmeApplet = new JSApplet.JSME("jsme", width + "px", height + "px", {
                "options": options
            });

            isInitialized = true;
            console.log(`JSME initialized with dimensions: ${width}x${height}`);

            // set up callback for structure changes - whenever a molecular structure changes within the editor, onMoleculeChanged() will be called
            jsmeApplet.setCallBack("AfterStructureModified", function(jsmeEvent) {
                onMoleculeChanged();
            });

            // load default SMILES if provided
            if (defaultSmiles && defaultSmiles.trim() !== "") {
                setTimeout(() => {
                    try {
                        jsmeApplet.readGenericMolecularInput(defaultSmiles);
                        console.log("Loaded default SMILES:", defaultSmiles);
                    } catch (error) {
                        console.error("Error loading default SMILES:", error);
                    }
                }, 100);
            }

            Streamlit.setFrameHeight(height + 80);

        }, 50); // small delay to ensure cleanup

    } catch (error) {
        console.error("Error initializing JSME:", error);
    }
}

// Called when molecule structure changes in JSME, handle data transfer from Custom Component to Streamlit
function onMoleculeChanged() {
    if (!jsmeApplet || !isInitialized) {
        console.log("JSME not ready yet");
        return;
    }

    try {
        // extract current molecule structure
        const smiles = jsmeApplet.smiles();
        const molfile = jsmeApplet.molFile();
        const jme = jsmeApplet.jmeFile();

        console.log("Molecule changed - SMILES:", smiles);

        // wrap the retrieved values in an object
        const moleculeData = {
            smiles: smiles || "",
            molfile: molfile || "",
            jme: jme || ""
        };

        // send the object back to Streamlit so we can retrieve the values from moleculeData on Streamlit Python side
        Streamlit.setComponentValue(moleculeData);

    } catch (error) {
        console.error("Error getting molecule data:", error);
        Streamlit.setComponentValue({
            smiles: "",
            molfile: "",
            jme: ""
        });
    }
}

// Handle data transfer from  Streamlit to Custom Component
function onDataFromPython(event) {
    const data = event.detail;
    console.log("Received data from Python:", data);

    const defaultSmiles = data.args.default_smiles || "";
    const width = data.args.width || 500;
    const height = data.args.height || 400;
    const options = data.args.options || "oldlook,star";

    // check if dimensions changed or JSME not initialized
    const dimensionsChanged = (width !== currentWidth || height !== currentHeight);
    const needsInitialization = !isInitialized || dimensionsChanged;

    if (needsInitialization) {
        // wait for JSME library to load, then initialize
        const checkJSME = setInterval(() => {
            if (window.JSApplet && window.JSApplet.JSME) {
                clearInterval(checkJSME);
                initializeJSME(defaultSmiles, width, height, options);
            }
        }, 100);

        // timeout after 10 seconds
        setTimeout(() => {
            clearInterval(checkJSME);
            if (!isInitialized) {
                console.error("JSME failed to load within 10 seconds");
            }
        }, 10000);
    } else if (defaultSmiles && defaultSmiles.trim() !== "") {
        // JSME already initialized with correct dimensions, just update SMILES
        try {
            jsmeApplet.readGenericMolecularInput(defaultSmiles);
            console.log("Updated JSME with new SMILES:", defaultSmiles);
        } catch (error) {
            console.error("Error updating JSME with new SMILES:", error);
        }
    }
}

// Setup event listeners
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded, setting up JSME component");
    Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onDataFromPython);
    Streamlit.setComponentReady();
});

// Fallback for already loaded DOM
if (document.readyState !== 'loading') {
    console.log("DOM already loaded, setting up JSME component immediately");
    Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onDataFromPython);
    Streamlit.setComponentReady();
}
