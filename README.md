*This guide was generated with the help of Codex*

# EduSpec

EduSpec is a Streamlit application for practicing spectroscopy questions. It supports IR, NMR, MS, combination exercises, normal text and multiple-choice questions, spectrum-click questions, and molecule drawing questions checked with SMILES.

## Setup And Run

### 1. Install Python

Install Python 3.12 or newer.

To check whether Python is available, open a terminal in the project folder and run:

```powershell
python --version
```

You should see something like `Python 3.12.x` or higher.

### 2. Open The Project Folder

All commands should be run from the root of this project. That is the folder that contains:

```text
README.md
pyproject.toml
src/
data/
tests/
```

### 3. Create A Virtual Environment

This keeps the app's Python packages separate from the rest of your computer.

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```cmd
.venv\Scripts\activate.bat
```

### 4. Install The App Dependencies

Run this from the project root:

```powershell
python -m pip install -e .
```

This installs Streamlit and the other packages listed in `pyproject.toml`.

### 5. Start The Application

Run Streamlit from the project root:

```powershell
python -m streamlit run src/main.py
```

Streamlit will print a local URL, usually:

```text
http://localhost:8501
```

Open that URL in your browser.

### 6. Stop The Application

Go back to the terminal where Streamlit is running and press:

```text
Ctrl + C
```

## Project Folders

The most important folders for content editors are:

```text
data/questions/     Question JSON files
data/navigation/    Sidebar navigation JSON
data/images/        Image files used by questions
data/molecules/     Molecule files used as 3D figures
data/spectra/       IR, NMR, and MS spectral data files
src/                Application code
```

## Creating A New Question

Every question is stored as one JSON file in:

```text
data/questions/
```

The file name should match the question `id`.

For example, this question:

```json
{
  "id": "ir_example_question"
}
```

should be saved as:

```text
data/questions/ir_example_question.json
```

Use simple, unique IDs with lowercase letters, numbers, and underscores. Good examples:

```text
ir_carbonyl_click
nmr_methyl_triplet
combo_draw_ethanol
```

Avoid spaces in IDs.

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

### Body Format

`bodyFormat` controls how the question instructions are displayed, is optional and defaults to latex.

Use normal text for simple prompts:

```json
"bodyFormat": "text"
```

Use LaTeX formatting when the prompt contains formulas, units, isotopes, subscripts, superscripts, or simple math:

```json
"bodyFormat": "latex"
```

When `bodyFormat` is `"latex"`, write LaTeX math between dollar signs inside `bodyText`:

```json
{
  "bodyText": "Unknown A has formula $C_4H_{10}O$. Click the band near $1245\\ cm^{-1}$.",
  "bodyFormat": "latex"
}
```

Important details:

- In the JSON file, the field is named `bodyFormat`.
- In the Python code, this becomes `body_format`.
- If `bodyFormat` is left out, the app treats it as `"latex"`.
- In JSON strings, write a backslash as `\\`. For example, use `$1245\\ cm^{-1}$`, not `$1245\ cm^{-1}$`.
- Do not use LaTeX packages such as `mhchem`; keep formulas simple, such as `$C_4H_{10}O$`, `$CH_3$`, `$^1H$`, and `$m/z$`.

### Figures

`figures` is always a list. It can be empty:

```json
"figures": []
```

Or it can contain one or more figures:

```json
"figures": [
  {
    "path": "data/images/test.png",
    "description": "Description shown below the image."
  },
  {
    "path": "data/molecules/water.pdb",
    "description": "Description shown below the 3D molecule viewer."
  }
]
```

Use image files for normal figures, such as `.png`, `.jpg`, or `.jpeg`.

Use molecule files from `data/molecules/` for 3D molecule figures. The current app renders `.pdb` and `.ent` files as 3D molecule viewers.

A question can have multiple figures. The app displays them in two columns.

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
      "path": "data/images/test.png",
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

- `answers` is the list of choices.
- `correctAnswer` is the number of the correct answer, starting at `0`.
- `feedbacks` must have the same number of items as `answers`.

Example: if the first answer is correct, use `"correctAnswer": 0`.

### Integer Or Number Range

The student enters a number. The answer is correct if it is between `lowerBound` and `upperBound`.

```json
{
  "id": "ms_base_peak_range",
  "title": "MS: Read the Base Peak m/z",
  "bodyText": "Enter the $m/z$ value of the base peak.",
  "bodyFormat": "latex",
  "figures": [
    {
      "path": "data/images/test.png",
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

- The correct answer is a range.
- `feedbacks` must contain exactly three items:
  - correct feedback
  - too low feedback
  - too high feedback

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

- The answer must match `correctAnswer`.
- Keep answers simple, because this question type checks text directly.

### Spectral

The student clicks a point in a spectrum. This is used for IR, NMR, and MS questions.

```json
{
  "id": "ir_c_o_stretch_click",
  "title": "IR: Click the Strong C-O Stretch",
  "bodyText": "Click the deepest C-O stretching absorption near $1245\\ cm^{-1}$.",
  "bodyFormat": "latex",
  "figures": [
    {
      "path": "data/images/test.png",
      "description": "Mock IR spectrum."
    }
  ],
  "version": 1,
  "type": "spectral",
  "spectralpath": "data/spectra/ir.dx",
  "correctAnswer": 1245.0,
  "feedbacks": [
    "Correct.",
    "Not quite. Look near 1245 cm^-1."
  ],
  "tolerance": 8.0
}
```

Important details:

- `spectralpath` points to the spectrum file.
- The app detects the spectrum type from the file path:
  - path containing `ir` becomes an IR spectrum
  - path containing `nmr` becomes an NMR spectrum
  - path containing `ms` becomes an MS spectrum
- `correctAnswer` is the x-axis value the student should click.
- `tolerance` is how far away the click may be and still count as correct.
- `feedbacks` has two items:
  - correct feedback
  - incorrect feedback

### Molecule Drawing

The student draws a molecule. The drawing is converted to a SMILES string and checked against `correctAnswer`.

```json
{
  "id": "combo_draw_butanol",
  "title": "Combination A: Draw the Molecule",
  "bodyText": "Draw 1-butanol, $C_4H_{10}O$, in the molecule editor.",
  "bodyFormat": "latex",
  "figures": [
    {
      "path": "data/images/test.png",
      "description": "Mock evidence panel."
    },
    {
      "path": "data/molecules/water.pdb",
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
- `defaultAnswer` is what appears in the editor at the start. Use `""` for a blank editor.
- `widgetKey` must be unique for every drawing question.

## Adding A Question To Navigation

The sidebar navigation is stored in:

```text
data/navigation/navigation.json
```

The top-level `items` become the main sidebar tabs. For example:

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

Each navigation entry must have either:

- `children`, if it is a folder/group
- `question`, if it opens a question

It must not have both.

### Folder Entry

Use a folder entry when you want to group questions:

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

### Question Entry

Use a question entry when clicking it should open a question:

```json
{
  "label": "C-O Stretch",
  "question": "ir_c_o_stretch_click"
}
```

The value of `question` must match the `id` of a file in `data/questions/`.

For example:

```json
"question": "ir_c_o_stretch_click"
```

loads:

```text
data/questions/ir_c_o_stretch_click.json
```

### Full Navigation Example

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
      "label": "NMR",
      "children": [
        {
          "label": "1H NMR Basics",
          "children": [
            {
              "label": "Chemical Shift",
              "question": "nmr_oxygen_shift_mcq"
            }
          ]
        }
      ]
    }
  ]
}
```

## Checklist For Adding Content

1. Add any needed files:
   - images to `data/images/`
   - molecule files to `data/molecules/`
   - spectrum files to `data/spectra/`
2. Create a new question JSON file in `data/questions/`.
3. Make sure the file name matches the question `id`.
4. Add a navigation entry in `data/navigation/navigation.json`.
5. Start the app with:

```powershell
python -m streamlit run src/main.py
```

6. Open the question from the sidebar and check:
   - the title appears
   - figures load
   - spectrum files load, if used
   - answer checking works

## Common Mistakes

### The Question Does Not Appear In The Sidebar

Check that the question was added to:

```text
data/navigation/navigation.json
```

### The App Says The Question Does Not Exist

Check that the `question` value in navigation matches the question file name.

For example, this navigation entry:

```json
{
  "label": "Example",
  "question": "my_question"
}
```

requires this file:

```text
data/questions/my_question.json
```

and the JSON inside should contain:

```json
{
  "id": "my_question"
}
```

### The Navigation File Breaks

Make sure every navigation item has either `question` or `children`, not both.

Correct:

```json
{
  "label": "Example Question",
  "question": "example_question"
}
```

Correct:

```json
{
  "label": "Example Folder",
  "children": []
}
```

Incorrect:

```json
{
  "label": "Broken Entry",
  "question": "example_question",
  "children": []
}
```

### A Figure Does Not Load

Check the path. Paths should normally start from the project root:

```json
{
  "path": "data/images/test.png",
  "description": "Example image."
}
```

### A Spectrum Question Does Not Load

Check that:

- `spectralpath` points to an existing file
- the path contains `ir`, `nmr`, or `ms`
- `correctAnswer` is a number with a decimal, such as `1245.0`
- `tolerance` is a number with a decimal, such as `8.0`

## Running Tests

Tests are optional for content editors, but useful after changing code.

Run all tests:

```powershell
python -m pytest
```

Run only the navigation tests:

```powershell
python -m pytest tests/streamlit/test_navigation.py
```

## Code Style

For code changes, use:

- `snake_case` for variables
- `camelCase` for functions
- `PascalCase` for classes
- Google-style docstrings
- type hints for function parameters and return types
