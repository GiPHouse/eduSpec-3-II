from typing import Any

import streamlit as st

from questions.Question import Question
from Script import Script


class ScriptQuestion(Question):
    """Question type that runs a custom Python script using user parameters."""

    def __init__(
        self,
        name: str,
        title: str,
        bodytext: str,
        script: Script,
        parameters: list[dict[str, Any]],
        checker: Any | None = None,
        figures: list[dict] | None = None,
        body_format: str = "text",
        download_data: str | None = None,
    ) -> None:
        """Initialise a script-based question.

        Args:
            name: Unique identifier for the question.
            title: Title shown to the user.
            bodytext: Main question text.
            script: Script object used to process the user's input.
            parameters: List of parameter definitions used by the script.
            checker: Optional checker used to verify the answer.
            figures: Optional list of figures to display with the question.
            body_format: Format of the body text, either "text" or "latex".
            download_data: Optional data that can be offered as a download.
        """
        super().__init__(
            name=name,
            title=title,
            bodytext=bodytext,
            checker=checker,
            figures=figures,
            body_format=body_format,
            download_data=download_data,
        )
        self.script = script
        self.parameters = parameters
        self.last_script_output: dict[str, Any] | None = None

    def drawYourself(self) -> dict[str, Any]:
        """Draw parameter input widgets and return the collected values."""
        values: dict[str, Any] = {}

        for parameter in self.parameters:
            param_name = parameter["name"]
            label = parameter.get("label", param_name)
            input_type = parameter.get("inputType", "text")
            default = parameter.get("default")
            key = self._paramKey(param_name)

            match input_type:
                case "integer":
                    values[param_name] = st.number_input(
                        label,
                        value=int(default) if default is not None else 0,
                        step=1,
                        key=key,
                    )

                case "number":
                    values[param_name] = st.number_input(
                        label,
                        value=float(default) if default is not None else 0.0,
                        key=key,
                    )

                case "slider":
                    min_value = parameter.get("min", 0)
                    max_value = parameter.get("max", 100)
                    value = parameter.get("default", min_value)
                    step = parameter.get("step", 1)

                    values[param_name] = st.slider(
                        label,
                        min_value=min_value,
                        max_value=max_value,
                        value=value,
                        step=step,
                        key=key,
                    )

                case "checkbox":
                    values[param_name] = st.checkbox(
                        label,
                        value=bool(default) if default is not None else False,
                        key=key,
                    )

                case "select":
                    options = parameter.get("options", [])
                    default_index = 0

                    if default in options:
                        default_index = options.index(default)

                    values[param_name] = st.selectbox(
                        label,
                        options,
                        index=default_index,
                        key=key,
                    )

                case "textarea":
                    values[param_name] = st.text_area(
                        label,
                        value=str(default) if default is not None else "",
                        key=key,
                    )

                case _:
                    values[param_name] = st.text_input(
                        label,
                        value=str(default) if default is not None else "",
                        key=key,
                    )

        return values

    def verifyAndFeedback(self, answer: dict[str, Any]) -> tuple[bool, str]:
        """Run the custom script and return correctness plus feedback."""
        try:
            result = self.script.run(answer)
        except Exception as error:
            self.last_script_output = None
            return False, f"The script could not run: {error}"

        correct = result.get("correct", True)
        feedback = result.get("feedback", "")

        if not isinstance(correct, bool):
            self.last_script_output = None
            return False, "The script result field 'correct' must be a boolean."

        if not isinstance(feedback, str):
            self.last_script_output = None
            return False, "The script result field 'feedback' must be a string."

        self.last_script_output = result.get("output")
        return correct, feedback

    def drawFeedbackResult(self) -> None:
        """Draw optional script output after feedback."""
        if not self.last_script_output:
            return

        output_type = self.last_script_output.get("type", "text")
        data = self.last_script_output.get("data")

        if data is None:
            return

        st.divider()

        match output_type:
            case "markdown":
                st.markdown(data)

            case "json":
                st.json(data)

            case "table":
                st.dataframe(data, use_container_width=True)

            case "line_chart":
                if isinstance(data, list) and data and isinstance(data[0], dict):
                    first_row = data[0]

                    if "x" in first_row and "y" in first_row:
                        st.line_chart(data, x="x", y="y")
                    else:
                        st.line_chart(data)
                else:
                    st.line_chart(data)

            case "bar_chart":
                if isinstance(data, list) and data and isinstance(data[0], dict):
                    first_row = data[0]

                    if "x" in first_row and "y" in first_row:
                        st.bar_chart(data, x="x", y="y")
                    else:
                        st.bar_chart(data)
                else:
                    st.bar_chart(data)

            case "scatter_chart":
                if hasattr(st, "scatter_chart"):
                    st.scatter_chart(data)
                else:
                    st.warning("scatter_chart is not available in this Streamlit version.")
                    st.dataframe(data, use_container_width=True)

            case "pyplot":
                st.pyplot(data)

            case _:
                st.write(data)

    def resetSessionState(self) -> None:
        """Reset parameter widgets to their default values."""
        for parameter in self.parameters:
            param_name = parameter["name"]
            key = self._paramKey(param_name)

            if key in st.session_state:
                del st.session_state[key]

        self.last_script_output = None

    def _paramKey(self, param_name: str) -> str:
        """Create a unique Streamlit key for one parameter."""
        return f"{self.name}_{param_name}"
