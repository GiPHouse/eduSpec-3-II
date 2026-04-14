from streamlit.testing.v1 import AppTest


def get_button_by_label(at: AppTest, label: str) -> object:
    """Return the first button whose label matches the given text."""
    return next(button for button in at.button if button.label == label)


def all_text_content(at: AppTest) -> str:
    """Collect visible text-like content from the rendered app."""
    parts = []
    parts.extend(element.value for element in at.title)
    parts.extend(element.value for element in at.text)
    parts.extend(element.value for element in at.markdown)
    parts.extend(element.value for element in at.info)
    parts.extend(element.value for element in at.success)
    parts.extend(element.value for element in at.error)
    return " ".join(str(part) for part in parts)
