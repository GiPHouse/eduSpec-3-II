# EduSpec

EduSpec is a Streamlit learning environment for spectroscopy practice. It supports standalone questions, multi-question quizzes, IR/NMR/MS spectrum-click exercises, text and numeric answers, multiple choice answers, molecule drawing with JSME, custom Python checkers, and script-driven interactive questions.

The application reads course content from a data directory, so the app code and the teaching material can be managed separately. The default data directory is `data/`, but deployments can point EduSpec at another folder or clone a content repository at container startup.

## Table of Contents

- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Running With Docker](#running-with-docker)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Data Directory Structure](#data-directory-structure)
- [Assets And File Paths](#assets-and-file-paths)
- [Creating Questions](#creating-questions)
- [Shared Question Fields](#shared-question-fields)
- [Question Types](#question-types)
- [Quizzes](#quizzes)
- [Navigation](#navigation)
- [Custom Checkers](#custom-checkers)
- [Script Questions](#script-questions)
- [Content Editor](#content-editor)
- [Content Checklist](#content-checklist)
- [Troubleshooting](#troubleshooting)
- [Running Tests](#running-tests)
- [Code Style](#code-style)

## Requirements

- Python 3.12 or newer
- A browser
- Docker or Podman, if you want to run the containerized app

Check Python with:

```powershell
python --version
```

The project dependencies are listed in `pyproject.toml`. The main runtime dependencies are Streamlit, Plotly, JCAMP parsing, `stmol`, and `py3Dmol`.

## Quick Start

Run all commands from the project root unless a command says otherwise. The project root is the folder that contains `README.md`, `pyproject.toml`, `src/`, `data/`, and `tests/`.

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

Install the app in editable mode:

```powershell
python -m pip install -e .
```

Start the learner app:

```powershell
python -m streamlit run src/main.py
```

Streamlit will print a local URL, usually:

```text
http://localhost:8501
```

Stop the app with `Ctrl + C` in the terminal where Streamlit is running.

## Running With Docker

Build and run the learner app with Docker Compose:

```powershell
docker compose up --build eduspec
```

The learner app is served on:

```text
http://localhost:8501
```

Run the content editor service with:

```powershell
docker compose up --build eduspec-editor
```

The editor is served on:

```text
http://localhost:8502
```

The Compose setup mounts the local `data/` directory into the container. The learner app uses it read-only; the editor uses it read-write.

You can also build and run the image manually:

```powershell
docker build -t eduspec .
docker run -p 8501:8501 -v ${PWD}\data:/data:ro -e EDUSPEC_DATA_DIR=/data eduspec
```

On Linux or macOS, the volume syntax is:

```sh
docker run \
  -p 8501:8501 \
  -e EDUSPEC_DATA_DIR=/data \
  -v "$PWD/data:/data:ro" \
  eduspec
```

With Podman on SELinux-enabled systems, add the `Z` mount option:

```sh
podman run \
  -p 8501:8501 \
  -e EDUSPEC_DATA_DIR=/data \
  -v "$PWD/data:/data:ro,Z" \
  eduspec
```

## Configuration

EduSpec uses these environment variables:

| Variable | Purpose |
| --- | --- |
| `EDUSPEC_DATA_DIR` | Root directory for content. Defaults to the project's `data/` folder locally and `/data` in Docker. |
| `DATA_DIR` | Backward-compatible fallback for the data directory. |
| `PATH_FROM_ROOT` | Older fallback for the data directory. Prefer `EDUSPEC_DATA_DIR`. |
| `EDUSPEC_NAVIGATION_FILE` | Optional override for the navigation JSON file. Defaults to `<data-dir>/navigation/navigation.json`. |
| `EDUSPEC_DATA_GIT_URL` | Optional Git repository URL to clone into the data directory before the container starts. |
| `EDUSPEC_DATA_GIT_REF` | Optional branch or tag to use with `EDUSPEC_DATA_GIT_URL`. |
| `MAIN_FILE` | Docker entrypoint setting for the Streamlit file. Defaults to `main.py`. |
| `PORT` | Docker entrypoint setting for the Streamlit port. Defaults to `8501`. |

To run locally with a separate content folder:

```powershell
$env:EDUSPEC_DATA_DIR = "C:\path\to\course-data"
python -m streamlit run src/main.py
```

To use a custom navigation file:

```powershell
$env:EDUSPEC_NAVIGATION_FILE = "C:\path\to\navigation.json"
python -m streamlit run src/main.py
```

In Git-backed Docker mode, the target data directory must be empty before startup:

```sh
docker run \
  -p 8501:8501 \
  -e EDUSPEC_DATA_GIT_URL=https://github.com/example/course-data.git \
  -e EDUSPEC_DATA_GIT_REF=main \
  eduspec
```

## Project Structure

```text
src/                    Streamlit application code
src/main.py             Learner app entry point
src/editor/editor.py    Content editor entry point
data/                   Example/default content
tests/                  Unit and Streamlit tests
Dockerfile              Container image definition
compose.yaml            Learner and editor Compose services
pyproject.toml          Python package metadata, dependencies, and test config
```

## Data Directory Structure

A data directory can be the built-in `data/` folder or any folder selected with `EDUSPEC_DATA_DIR`.

```text
data/
  questions/      Question JSON files
  quizzes/        Quiz JSON files
  navigation/     Sidebar navigation JSON
  images/         Image assets: .png, .jpg, .jpeg
  molecules/      Molecule assets: .pdb now, .mol after the pending molecule-file PR
  spectra/        Spectrum assets: .dx, .jdx
  compressed/     Downloadable .zip files
  checkers/       Custom checker Python files
  scripts/        Custom script-question Python files
```

## Assets And File Paths

Question files can refer to assets by filename or by a path. Prefer short paths relative to the relevant asset folder when possible:

```json
{
  "path": "test.png",
  "description": "Image shown above the question."
}
```

Useful examples:

```text
test.png
water.pdb
ir.dx
nmr.jdx
easy001/ir.dx
ziptest.zip
```

Short paths are resolved by the file manager based on extension. For example, `test.png` resolves under `images/`, `water.pdb` resolves under `molecules/`, and `easy001/ir.dx` resolves under `spectra/`. Existing absolute paths can also be used.

Supported content-manager file types:

| Type | Extensions | Default folder |
| --- | --- | --- |
| Images | `.png`, `.jpg`, `.jpeg` | `images/` |
| Molecules | `.pdb`, `.mol` | `molecules/` |
| Spectra | `.dx`, `.jdx` | `spectra/` |
| Downloads | `.zip` | `compressed/` |

For molecule figures, `.pdb` is supported in the current app. `.mol` files are included here because they are expected to be supported by the PR that is about to be merged. Put both file types in `data/molecules/`.

## Creating Questions

Every question is stored as one JSON file in:

```text
data/questions/
```

The filename should match the question `id`:

```json
{
  "id": "ir_example_question"
}
```

Save it as:

```text
data/questions/ir_example_question.json
```

Use simple, unique IDs with lowercase letters, numbers, and underscores:

```text
ir_carbonyl_click
nmr_methyl_triplet
combo_draw_ethanol
```

Avoid spaces in IDs. IDs are also used in navigation and quiz files.

## Shared Question Fields

All question types use these fields:

```json
{
  "id": "unique_question_id",
  "title": "Title shown at the top of the page",
  "bodyText": "Instructions shown to the student.",
  "bodyFormat": "text",
  "figures": [],
  "version": 1,
  "type": "question_type"
}
```

Optional shared fields:

```json
{
  "checker": "custom_checker_module",
  "download_data": "ziptest.zip"
}
```

| Field | Required | Notes |
| --- | --- | --- |
| `id` | Yes | Unique question ID. |
| `title` | Yes | Displayed as the question title. |
| `bodyText` | Yes | Main prompt. |
| `bodyFormat` | No | `"text"` or `"latex"`. Defaults to `"text"` when omitted. |
| `figures` | Yes | Use `[]` when there are no figures. |
| `version` | Yes | Current question JSON version is `1`. |
| `type` | Yes | One of `multipleChoice`, `integer`, `word`, `spectral`, `drawing`, or `script`. |
| `checker` | No | Custom checker module from `data/checkers/`. |
| `download_data` | No | Adds a download button for a file that can be loaded by `FigureManager`, such as a `.zip`, image, or spectrum file. |

### Body Format

Use `"text"` for plain prompts:

```json
"bodyFormat": "text"
```

Use `"latex"` when the prompt contains formulas, units, isotopes, subscripts, superscripts, or simple math:

```json
{
  "bodyText": "Unknown A has formula $C_4H_{10}O$. Click the band near $1245\\ cm^{-1}$.",
  "bodyFormat": "latex"
}
```

Important details:

- The JSON field is named `bodyFormat`.
- In Python, this becomes `body_format`.
- If `bodyFormat` is omitted, the app uses `"text"`.
- In JSON strings, write a backslash as `\\`.
- Keep LaTeX simple. Do not rely on extra LaTeX packages.

### Figures

`figures` is always a list. Use an empty list if the question has no figures:

```json
"figures": []
```

Each figure has a `path` and `description`:

```json
"figures": [
  {
    "path": "test.png",
    "description": "Image shown below the question title."
  },
  {
    "path": "water.pdb",
    "description": "3D molecule figure."
  }
]
```

The app displays figures in two columns. Normal image files are rendered as images. Molecule files are rendered in the 3D molecule viewer when supported by the active branch.

## Question Types

### Multiple Choice

The student chooses one answer from a list.

```json
{
  "id": "ir_broad_oh_mcq",
  "title": "IR: Recognize a Broad O-H Band",
  "bodyText": "Which functional group best explains a broad absorption around $3200$-$3600\\ cm^{-1}$?",
  "bodyFormat": "latex",
  "figures": [
    {
      "path": "test.png",
      "description": "Mock IR spectrum showing a broad O-H absorption."
    }
  ],
  "version": 1,
  "type": "multipleChoice",
  "answers": [
    "Alcohol O-H",
    "Nitrile C=N",
    "Alkene C=C",
    "Aromatic C-H only"
  ],
  "correctAnswer": 0,
  "feedbacks": [
    "Correct.",
    "A nitrile would be sharp near 2250 cm^-1.",
    "An alkene C=C stretch appears lower and is not broad.",
    "Aromatic C-H bands are not broad in this region."
  ]
}
```

Important details:

- `answers` must contain at least two choices.
- `correctAnswer` is zero-based. The first answer is `0`.
- `feedbacks` must have the same number of items as `answers`.

### Integer Or Number Range

The student enters a number. The answer is correct if it is between `lowerBound` and `upperBound`, inclusive.

```json
{
  "id": "ms_base_peak_range",
  "title": "MS: Read the Base Peak m/z",
  "bodyText": "Enter the $m/z$ value of the base peak.",
  "bodyFormat": "latex",
  "figures": [
    {
      "path": "test.png",
      "description": "Mock mass spectrum with a clear base peak."
    }
  ],
  "version": 1,
  "type": "integer",
  "lowerBound": 42.5,
  "upperBound": 43.5,
  "feedbacks": [
    "Correct.",
    "Too low.",
    "Too high."
  ]
}
```

Important details:

- Bounds may be integers or floats.
- `lowerBound` must be less than or equal to `upperBound`.
- `feedbacks` must contain exactly three items: correct, too low, too high.

### Word

The student types a word or short text answer.

```json
{
  "id": "nmr_terminal_methyl_word",
  "title": "NMR: Terminal Methyl Multiplicity",
  "bodyText": "A terminal $CH_3$ group next to a $CH_2$ group follows the $n+1$ rule. Type the expected multiplicity as one word.",
  "bodyFormat": "latex",
  "figures": [],
  "version": 1,
  "type": "word",
  "correctAnswer": "triplet",
  "correctFeedback": "Correct.",
  "incorrectFeedback": "Not quite. A CH3 next to a CH2 is split into a triplet."
}
```

Important details:

- The answer is compared directly to `correctAnswer`.
- Keep answers simple and consistent with spelling and capitalization expected from students.

### Spectral

The student clicks a peak or point in a spectrum. This is used for IR, NMR, and MS questions.

```json
{
  "id": "ir_c_o_stretch_click",
  "title": "IR: Click the Strong C-O Stretch",
  "bodyText": "Click the deepest C-O stretching absorption near $1245\\ cm^{-1}$.",
  "bodyFormat": "latex",
  "figures": [
    {
      "path": "test.png",
      "description": "Mock IR spectrum."
    }
  ],
  "version": 1,
  "type": "spectral",
  "spectralpath": "ir.dx",
  "correctAnswer": 1245.0,
  "feedbacks": [
    "Correct.",
    "Not quite. Look near 1245 cm^-1."
  ],
  "tolerance": 8.0
}
```

Important details:

- `spectralpath` points to a `.dx` or `.jdx` file.
- `correctAnswer` and `tolerance` must be floats, such as `1245.0` and `8.0`.
- `feedbacks` has two items: correct and incorrect.
- Spectrum type is detected from JCAMP metadata first. If metadata is incomplete, the app falls back to the filename or path containing `ir`, `nmr`, or `ms`.
- IR and NMR line plots snap selected points to nearby peaks. MS spectra are displayed as bars.

### Molecule Drawing

The student draws a molecule in the JSME editor. The drawn molecule is submitted as a SMILES string and checked against `correctAnswer`.

```json
{
  "id": "combo_draw_butanol",
  "title": "Combination A: Draw the Molecule",
  "bodyText": "Draw 1-butanol, $C_4H_{10}O$, in the molecule editor.",
  "bodyFormat": "latex",
  "figures": [
    {
      "path": "test.png",
      "description": "Evidence panel."
    },
    {
      "path": "water.pdb",
      "description": "Example 3D molecule figure."
    }
  ],
  "version": 1,
  "type": "drawing",
  "correctAnswer": "CCCCO",
  "defaultAnswer": "",
  "correctFeedback": "Correct.",
  "incorrectFeedback": "Not quite. Draw a straight four-carbon chain with OH on carbon 1.",
  "widgetKey": "combo_draw_butanol_editor"
}
```

Important details:

- `correctAnswer` is the expected SMILES string.
- `defaultAnswer` is the starting SMILES in the editor. Use `""` for a blank editor.
- `widgetKey` must be a string and should be unique for every drawing question.
- The current comparison is direct string comparison unless a custom checker is used.

### Script

Script questions draw one or more input widgets, pass the collected values to a Python script, and display the returned feedback and optional output.

```json
{
  "id": "script_peak_ratio",
  "title": "Script: Peak Ratio",
  "bodyText": "Choose values and submit.",
  "bodyFormat": "text",
  "figures": [],
  "version": 1,
  "type": "script",
  "script": "PeakRatio.py",
  "parameters": [
    {
      "name": "peak_a",
      "label": "Peak A",
      "inputType": "number",
      "default": 1.0
    },
    {
      "name": "mode",
      "label": "Mode",
      "inputType": "select",
      "options": ["strict", "lenient"],
      "default": "strict"
    }
  ]
}
```

Supported parameter `inputType` values:

```text
text
textarea
number
integer
slider
checkbox
select
```

For `slider`, you can use `min`, `max`, `default`, and `step`. For `select`, `options` must be a non-empty list.

See [Script Questions](#script-questions) for the Python script format.

## Quizzes

Quizzes are stored in:

```text
data/quizzes/
```

A quiz JSON file lists question IDs in order:

```json
{
  "id": "combination1",
  "questionNames": [
    "combo_unknown_a_ir",
    "nmr_methyl_triplet_click",
    "ms_base_peak_click",
    "combo_unknown_a_mcq",
    "combo_draw_butanol"
  ]
}
```

Save this as:

```text
data/quizzes/combination1.json
```

The quiz UI tracks attempts, lets students jump between numbered questions, shows an overview, and displays a final review page once every question has been attempted.

## Navigation

The sidebar navigation is stored in:

```text
data/navigation/navigation.json
```

The top-level `items` become sidebar tabs:

```json
{
  "items": [
    {
      "label": "IR",
      "children": []
    },
    {
      "label": "NMR",
      "children": []
    }
  ]
}
```

Navigation entries can point to a question, a quiz, or a group of child entries.

Question entry:

```json
{
  "label": "C-O Stretch",
  "question": "ir_c_o_stretch_click"
}
```

Quiz entry:

```json
{
  "label": "Combination quiz",
  "quiz": "combination1"
}
```

Folder entry:

```json
{
  "label": "Functional Groups",
  "children": [
    {
      "label": "C-O Stretch",
      "question": "ir_c_o_stretch_click"
    }
  ]
}
```

Full example:

```json
{
  "items": [
    {
      "label": "IR",
      "children": [
        {
          "label": "Functional Groups",
          "children": [
            {
              "label": "C-O Stretch",
              "question": "ir_c_o_stretch_click"
            },
            {
              "label": "Broad O-H Pattern",
              "question": "ir_broad_oh_mcq"
            }
          ]
        }
      ]
    },
    {
      "label": "Combination exercises",
      "children": [
        {
          "label": "Unknown A",
          "children": [
            {
              "label": "Combination quiz",
              "quiz": "combination1"
            },
            {
              "label": "Draw 1-butanol",
              "question": "combo_draw_butanol"
            }
          ]
        }
      ]
    }
  ]
}
```

Direct links are also supported through query parameters:

```text
http://localhost:8501/?question=ir_c_o_stretch_click
http://localhost:8501/?quiz=combination1
http://localhost:8501/?page=about
```

## Custom Checkers

Custom checkers live in:

```text
data/checkers/
```

Use a checker when the built-in answer comparison is not enough. The question JSON references the checker module name without `.py`:

```json
{
  "id": "question_custom_checker",
  "title": "Custom range",
  "bodyText": "Enter a number.",
  "version": 1,
  "type": "integer",
  "figures": [],
  "checker": "customintchecker"
}
```

The checker file must define a callable `check` function with the return annotation `tuple[bool, str]`:

```python
def check(answer: int) -> tuple[bool, str]:
    if answer < 50:
        return False, "Too low!"
    if answer > 100:
        return False, "Too high!"
    return True, "Juuust right!"
```

When `checker` is set, the app delegates answer checking to the custom function. Some question types still require display-related fields. For example, multiple-choice questions still need `answers`, and drawing questions still need `defaultAnswer` and `widgetKey`.

## Script Questions

Script-question Python files live in:

```text
data/scripts/
```

The script must define:

```python
def run(params: dict) -> dict:
    return {
        "correct": True,
        "feedback": "Correct.",
        "output": {
            "type": "markdown",
            "data": "**Optional extra output**"
        }
    }
```

The `params` dictionary contains the submitted values keyed by the `name` fields from the question JSON.

The result dictionary supports:

| Key | Required | Notes |
| --- | --- | --- |
| `correct` | No | Boolean. Defaults to `True` if omitted. |
| `feedback` | No | String. Defaults to `""` if omitted. |
| `output` | No | Optional extra content displayed after feedback. |

Supported output `type` values:

```text
text
markdown
json
table
line_chart
bar_chart
scatter_chart
pyplot
```

For chart and table outputs, pass data in a shape accepted by the corresponding Streamlit function.

## Content Editor

The repository includes an experimental Streamlit editor for creating question files and uploading assets.

With Docker Compose:

```powershell
docker compose up --build eduspec-editor
```

Open:

```text
http://localhost:8502
```

For local development, run the editor from the `src/` directory so its relative upload paths point back to the project `data/` folder:

```powershell
cd src
python -m streamlit run editor/editor.py --server.port 8502
```

The editor is intended to help create integer, word, multiple-choice, spectral, and drawing questions. It uploads image files, spectra, `.pdb` molecule files, and `.mol` molecule files. After creating a question, check the generated JSON and add the question or quiz to `data/navigation/navigation.json` if needed.

## Content Checklist

1. Add required assets to the data directory:
   - images to `data/images/`
   - molecule files to `data/molecules/`
   - spectra to `data/spectra/`
   - downloadable ZIP files to `data/compressed/`
2. Create the question JSON file in `data/questions/`.
3. Make sure the question filename matches the question `id`.
4. Create or update quiz JSON files in `data/quizzes/`, if needed.
5. Add a navigation entry in `data/navigation/navigation.json`.
6. Start the app:

```powershell
python -m streamlit run src/main.py
```

Check that:

- The sidebar entry appears.
- The question or quiz opens.
- Figures and downloads load.
- Spectra render and clicks are accepted, if used.
- Answer checking and feedback work.

## Troubleshooting

### The Question Does Not Appear In The Sidebar

Check that the question was added to:

```text
data/navigation/navigation.json
```

Also check that the entry uses `question`, not `quiz`, for standalone questions.

### The App Says The Question Does Not Exist

The navigation `question` value must match the JSON filename and the question `id`.

This entry:

```json
{
  "label": "Example",
  "question": "my_question"
}
```

requires:

```text
data/questions/my_question.json
```

and:

```json
{
  "id": "my_question"
}
```

### The App Says The Quiz Does Not Exist

The navigation `quiz` value must match a file in `data/quizzes/`.

```json
{
  "label": "Combination quiz",
  "quiz": "combination1"
}
```

requires:

```text
data/quizzes/combination1.json
```

### A Figure Does Not Load

Check that:

- The file exists in the active data directory.
- The extension is supported.
- The path is spelled exactly as it appears on disk.
- The `figures` field is a list, even for one figure.

Good:

```json
{
  "figures": [
    {
      "path": "test.png",
      "description": "Example image."
    }
  ]
}
```

### A Molecule Figure Does Not Render

Use `.pdb` files in the current app. `.mol` files should be placed in `data/molecules/` and are expected to work after the upcoming `.mol` support PR is merged.

### A Spectrum Question Does Not Load

Check that:

- `spectralpath` points to an existing `.dx` or `.jdx` file.
- The file has JCAMP metadata that identifies IR, NMR, or MS, or the path contains `ir`, `nmr`, or `ms`.
- `correctAnswer` is a float, such as `1245.0`.
- `tolerance` is a float, such as `8.0`.
- `feedbacks` has at least the correct and incorrect feedback messages.

### A Custom Checker Does Not Load

Check that:

- The checker file is in `data/checkers/`.
- The JSON value does not include `.py`.
- The checker defines `check(answer) -> tuple[bool, str]`.
- The return annotation is exactly `tuple[bool, str]`.

### Docker Git Mode Fails

If `EDUSPEC_DATA_GIT_URL` is set, the target `EDUSPEC_DATA_DIR` must be empty. Use an empty volume or remove the Git-mode environment variables and mount existing content instead.

## Running Tests

Run all tests:

```powershell
python -m pytest
```

Run unit tests:

```powershell
python -m pytest tests/unit
```

Run Streamlit-focused tests:

```powershell
python -m pytest tests/streamlit
```

Run only navigation tests:

```powershell
python -m pytest tests/streamlit/test_navigation.py
```

## Code Style

For code changes:

- Use type hints for function parameters and return types.
- Use Google-style docstrings.
- Prefer `snake_case` for variables.
- Existing code contains a mix of naming styles; follow nearby code when changing existing modules.
- Keep content JSON valid and formatted consistently.

Ruff configuration is stored in `pyproject.toml`.
