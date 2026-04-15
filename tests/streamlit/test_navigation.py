from streamlit.testing.v1 import AppTest


# =========================
# Navbar Tests
# =========================

def test_navbar_default_selection() -> None:
    """Test if the default selection is home"""
    at = AppTest.from_file("../../src/main.py")
    at.run()
    assert at.session_state["current_page"] == "Home"
    assert at.session_state["navbar"] == "Home"


def test_navbar_navigation_to_about() -> None:
    """Test navigation to About page"""
    at = AppTest.from_file("../../src/main.py")
    at.run()
    at.session_state["navbar"] = "About"
    assert at.session_state["navbar"] == "About"


def test_navbar_navigation_to_ir() -> None:
    """Test navigation to IR page"""
    at = AppTest.from_file("../../src/main.py")
    at.run()
    at.session_state["navbar"]= "IR"
    assert at.session_state["navbar"] == "IR"


def test_navbar_navigation_to_nmr() -> None:
    """Test navigation to NMR page"""
    at = AppTest.from_file("../../src/main.py")
    at.run()
    at.session_state["navbar"] = "NMR"
    assert at.session_state["navbar"] == "NMR"


def test_navbar_navigation_to_ms() -> None:
    """Test navigation to MS page"""
    at = AppTest.from_file("../../src/main.py")
    at.run()
    at.session_state["navbar"] = "MS"
    assert at.session_state["navbar"] == "MS"


def test_navbar_navigation_to_settings() -> None:
    """Test navigation to Settings page"""
    at = AppTest.from_file("../../src/main.py")
    at.run()
    at.session_state["navbar"] = "Settings"
    assert at.session_state["navbar"] == "Settings"


# =========================
# Sidebar Navigation Tests
# =========================

def test_sidebar_ir_spectral_areas() -> None:
    """Test sidebar navigation to IR Spectral Areas"""
    at = AppTest.from_file("../../src/main.py")
    at.run()
    
    at.session_state["navbar"] = "IR"
    at.button("IR Spectral Areas").click().run()
    
    assert at.session_state["navbar"] == "IR"
    assert at.session_state["current_page"] == "IR Spectral Areas"
    assert at.query_params["page"] == "IR Spectral Areas"


def test_sidebar_ir_theory() -> None:
    """Test sidebar navigation to IR Theory"""
    at = AppTest.from_file("../../src/main.py")
    at.run()
    
    at.session_state["navbar"] = "IR"
    at.button("IR Theory").click().run()
    
    assert at.session_state["current_page"] == "IR Theory"
    assert at.session_state["navbar"] == "IR"


def test_sidebar_ir_area_a() -> None:
    """Test sidebar navigation to IR Area A"""
    at = AppTest.from_file("../../src/main.py")
    at.run()
    
    at.session_state["navbar"] = "IR"
    at.button("IR Area A").click().run()
    
    assert at.session_state["current_page"] == "IR Area A"
    assert at.session_state["navbar"] == "IR"
    assert at.query_params["page"] == "IR Area A"


def test_sidebar_ir_area_a_quiz() -> None:
    """Test sidebar navigation to IR Area A Quiz"""
    at = AppTest.from_file("../../src/main.py")
    at.run()
    
    at.session_state["navbar"] = "IR"
    at.button("Spectral Areas").click().run()
    at.button("IR Area A").click().run()
    at.button("IR Area A Quiz").click().run()
    
    assert at.session_state["current_page"] == "IR Area A Quiz"
    assert at.session_state["navbar"] == "IR"
    assert at.query_params["page"] == "IR Area A Quiz"


def test_sidebar_ir_area_b() -> None:
    """Test sidebar navigation to IR Area B"""
    at = AppTest.from_file("../../src/main.py")
    at.run()
    
    at.session_state["navbar"] = "IR"
    at.button("IR Spectral Areas").click().run()
    at.button("IR Area B").click().run()
    
    assert at.session_state["current_page"] == "IR Area B"
    assert at.session_state["navbar"] == "IR"


def test_sidebar_ir_area_c() -> None:
    """Test sidebar navigation to IR Area C"""
    at = AppTest.from_file("../../src/main.py")
    at.run()
    
    at.session_state["navbar"] = "IR"
    at.button("IR Spectral Areas").click().run()
    at.button("IR Area C").click().run()
    
    assert at.session_state["current_page"] == "IR Area C"
    assert at.session_state["navbar"] == "IR"


def test_sidebar_ir_area_d() -> None:
    """Test sidebar navigation to IR Area D"""
    at = AppTest.from_file("../../src/main.py")
    at.run()
    
    at.session_state["navbar"] = "IR"
    at.button("IR Spectral Areas").click().run()
    at.button("IR Area D").click().run()
    
    assert at.session_state["current_page"] == "IR Area D"
    assert at.session_state["navbar"] == "IR"


# =========================
# URL Query Parameter Tests
# =========================

def test_url_direct_load_valid_page() -> None:
    """Test loading a valid page via URL query parameter"""
    at = AppTest.from_file("../../src/main.py")
    at.query_params["page"] = "IR Area B"
    at.run()
    assert at.session_state["current_page"] == "IR Area B"
    assert at.session_state["navbar"] == "IR"


def test_url_direct_load_with_none() -> None:
    """Test that page None defaults to Home"""
    at = AppTest.from_file("../../src/main.py")
    at.query_params["page"] = "None"
    at.run()
    assert at.session_state["current_page"] == "Home"
    assert at.session_state["navbar"] == "Home"


def test_url_direct_load_invalid_page() -> None:
    """Test that invalid page defaults to Home"""
    at = AppTest.from_file("../../src/main.py")
    at.query_params["page"] = "InvalidPage"
    at.run()
    assert at.session_state["current_page"] == "Home"
    assert at.session_state["navbar"] == "Home"


def test_url_direct_load_home() -> None:
    """Test loading Home page via URL"""
    at = AppTest.from_file("../../src/main.py")
    at.query_params["page"] = "Home"
    at.run()
    assert at.session_state["current_page"] == "Home"
    assert at.session_state["navbar"] == "Home"

# =========================
# Multiple Navigation Steps
# =========================

def test_multiple_navbar_navigations() -> None:
    """Test navigating through multiple navbar pages"""
    at = AppTest.from_file("../../src/main.py")
    at.run()
    
    # Navigate to IR
    at.session_state["navbar"] = "IR"
    assert at.session_state["current_page"] == "IR"
    assert at.session_state["navbar"] == "IR"
    
    # Navigate to NMR
    at.session_state["navbar"] = "NMR"
    assert at.session_state["current_page"] == "NMR"
    assert at.session_state["navbar"] == "NMR"
    
    # Navigate to About
    at.session_state["navbar"] = "About"
    assert at.session_state["current_page"] == "About"
    
    # Navigate back to Home
    at.session_state["navbar"] = "Home"
    assert at.session_state["navbar"] == "Home"
    assert at.session_state["current_page"] == "Home"


def test_navbar_to_sidebar_navigation_flow() -> None:
    """Test flowing from navbar click to sidebar click"""
    at = AppTest.from_file("../../src/main.py")
    at.run()
    
    # Start at Home
    assert at.session_state["current_page"] == "Home"
    
    # Click IR in navbar
    at.session_state["navbar"] = "IR"
    assert at.session_state["current_page"] == "IR"
    
    # Click IR Area A in sidebar
    at.button("IR Area A").click().run()
    assert at.session_state["current_page"] == "IR Area A"
    assert at.session_state["navbar"] == "IR"  # navbar stays on IR
    
    # Click IR Area B in sidebar
    at.button("IR Area B").click().run()
    assert at.session_state["current_page"] == "IR Area B"
    assert at.session_state["navbar"] == "IR"
