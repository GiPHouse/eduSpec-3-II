# Any custom script written or imported must have a callable run function for it to run.
# Along with a question that can be created using JSON

# example header: def run(params: dict[str, Any]) -> dict[str, Any]

# Below is an example of a script, and a question in JSON
"""from typing import Any

def run(params: dict[str, Any]) -> dict[str, Any]:
    name = str(params["name"]).strip()
    notes = str(params["notes"]).strip()
    a = float(params["a"])
    power = int(params["power"])
    x_max = int(params["x_max"])
    show_extra = bool(params["show_extra"])
    output_type = str(params["output_type"])

    points = []

    for x in range(0, x_max + 1):
        y = a * (x**power)
        points.append({"x": x, "y": y})

    if not name:
        return {
            "correct": False,
            "feedback": "Please enter your name first. This feedback comes from the custom script.",
            "output": {
                "type": "markdown",
                "data": "### Missing input\nThe script received an empty name.",
            },
        }

    feedback = (
        f"Hello {name}. The script received your inputs and calculated "
        f"y = {a} * x^{power} from x = 0 to x = {x_max}."
    )

    if notes:
        feedback += f" Your notes were also received: {notes}"

    if show_extra:
        feedback += " Extra information is enabled."

    if output_type == "text":
        output = {
            "type": "text",
            "data": f"Result: generated {len(points)} points.",
        }

    elif output_type == "markdown":
        output = {
            "type": "markdown",
            "data": (
                "### Script result\n"
                f"- Name: `{name}`\n"
                f"- Formula: `y = {a} * x^{power}`\n"
                f"- Number of points: `{len(points)}`"
            ),
        }

    elif output_type == "json":
        output = {
            "type": "json",
            "data": {
                "received_params": params,
                "generated_points": points,
                "point_count": len(points),
            },
        }

    elif output_type == "table":
        output = {
            "type": "table",
            "data": points,
        }

    elif output_type == "bar_chart":
        output = {
            "type": "bar_chart",
            "data": points,
        }

    else:
        output = {
            "type": "line_chart",
            "data": points,
        }

    return {
        "correct": True,
        "feedback": feedback,
        "output": output,
    }


"""

"""
{
  "id": "full_script_test_question",
  "title": "Full Script Question Test",
  "bodyText": "Fill in the parameters below. When you submit, a custom Python script will process your input, create custom feedback, and display the selected output type.",
  "bodyFormat": "text",
  "figures": [],
  "version": 1,
  "type": "script",
  "script": "full_script_test",
  "parameters": [
    {
      "name": "name",
      "label": "Your name",
      "inputType": "text",
      "default": ""
    },
    {
      "name": "notes",
      "label": "Optional notes",
      "inputType": "textarea",
      "default": "testing the script question"
    },
    {
      "name": "a",
      "label": "Coefficient a",
      "inputType": "number",
      "default": 1.0
    },
    {
      "name": "power",
      "label": "Power",
      "inputType": "integer",
      "default": 2
    },
    {
      "name": "x_max",
      "label": "Maximum x value",
      "inputType": "slider",
      "min": 1,
      "max": 20,
      "step": 1,
      "default": 10
    },
    {
      "name": "show_extra",
      "label": "Show extra feedback",
      "inputType": "checkbox",
      "default": true
    },
    {
      "name": "output_type",
      "label": "Output type",
      "inputType": "select",
      "default": "line_chart",
      "options": [
        "text",
        "markdown",
        "json",
        "table",
        "line_chart",
        "bar_chart"
      ]
    }
  ]
}

"""
