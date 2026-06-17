from typing import Any


def run(params: dict[str, Any]) -> dict[str, Any]:
    """Process the full script question demo parameters."""
    name = str(params["name"]).strip()
    notes = str(params["notes"]).strip()
    a = float(params["a"])
    power = int(params["power"])
    x_max = int(params["x_max"])
    show_extra = bool(params["show_extra"])
    output_type = str(params["output_type"])

    points = [{"x": x, "y": a * (x**power)} for x in range(0, x_max + 1)]

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
