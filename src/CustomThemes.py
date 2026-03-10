import streamlit as st

THEMES = {
    "Light": {
        "primaryColor": "#FF4B4B",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#F0F2F6",
        "textColor": "#262730",
        "buttonColor": "#FF4B4B",
        "inputBackground": "#FFFFFF",
        "borderColor": "#D3D3D3",
    },
    "Spotify": {
        "primaryColor": "#1DB954",
        "backgroundColor": "#121212",
        "secondaryBackgroundColor": "#1E1E1E",
        "textColor": "#FFFFFF",
        "buttonColor": "#1DB954",
        "inputBackground": "#2A2A2A",
        "borderColor": "#333333",
    },
    "Orange": {
        "primaryColor": "#F4845F",
        "backgroundColor": "#2D1B2E",
        "secondaryBackgroundColor": "#3D2440",
        "textColor": "#F2E8CF",
        "buttonColor": "#F4845F",
        "inputBackground": "#3D2440",
        "borderColor": "#7B4F6E",
    },
    "Blue Tint": {
        "primaryColor": "#5E9BF0",
        "backgroundColor": "#E8EEF7",
        "secondaryBackgroundColor": "#D1DDEF",
        "textColor": "#1A2744",
        "buttonColor": "#5E9BF0",
        "inputBackground": "#FFFFFF",
        "borderColor": "#A8C0E8",
    },
}


def applyTheme(theme: dict) -> None:
    """Applies a theme by injecting CSS into the Streamlit app."""
    st.html(
        f"""
        <style>
            /* Main background */
            .stApp {{
                background-color: {theme["backgroundColor"]};
                color: {theme["textColor"]};
            }}

            /* Sidebar */
            [data-testid="stSidebar"] {{
                background-color: {theme["secondaryBackgroundColor"]};
                border-right: 1px solid {theme["borderColor"]};
            }}

            /* All text */
            p, li, span, label {{
                color: {theme["textColor"]} !important;
            }}

            /* Buttons - primary */
            .stButton > button {{
                background-color: {theme["buttonColor"]};
                color: #FFFFFF !important;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                transition: opacity 0.2s ease;
            }}
            .stButton > button:hover {{
                opacity: 0.85;
                color: #FFFFFF !important;
            }}

            /* Secondary buttons */
            .stButton > button[kind="secondary"] {{
                background-color: transparent;
                color: {theme["primaryColor"]} !important;
                border: 1px solid {theme["primaryColor"]};
            }}

            /* Input fields */
            .stTextInput > div > div > input,
            .stNumberInput > div > div > input {{
                background-color: {theme["inputBackground"]};
                color: {theme["textColor"]};
                border: 1px solid {theme["borderColor"]};
                border-radius: 6px;
            }}

            /* Select boxes */
            .stSelectbox > div > div {{
                background-color: {theme["inputBackground"]};
                color: {theme["textColor"]};
                border: 1px solid {theme["borderColor"]};
                border-radius: 6px;
            }}

            /* Radio buttons */
            .stRadio > div {{
                color: {theme["textColor"]};
            }}
            .stRadio > div > label {{
                color: {theme["textColor"]} !important;
            }}

            /* Expanders */
            [data-testid="stExpander"] {{
                background-color: {theme["secondaryBackgroundColor"]};
                border: 1px solid {theme["borderColor"]};
                border-radius: 8px;
            }}

            /* Headers */
            h1, h2, h3, h4, h5, h6 {{
                color: {theme["textColor"]} !important;
            }}

            /* Divider */
            hr {{
                border-color: {theme["borderColor"]};
            }}

            /* Tabs */
            .stTabs [data-baseweb="tab"] {{
                color: {theme["textColor"]};
            }}
            .stTabs [aria-selected="true"] {{
                color: {theme["primaryColor"]} !important;
                border-bottom-color: {theme["primaryColor"]};
            }}

            /* Metric */
            [data-testid="stMetricValue"] {{
                color: {theme["primaryColor"]} !important;
            }}

            /* Code blocks */
            code {{
                background-color: {theme["secondaryBackgroundColor"]};
                color: {theme["primaryColor"]};
                border-radius: 4px;
                padding: 2px 4px;
            }}

            /* Containers / cards */
            [data-testid="stVerticalBlock"] > div {{
                border-radius: 8px;
            }}

            /* Success / info / warning / error boxes */
            .stAlert {{
                background-color: {theme["secondaryBackgroundColor"]};
                border: 1px solid {theme["borderColor"]};
                color: {theme["textColor"]};
                border-radius: 8px;
            }}
        </style>
        """,
    )


def showThemeSelector() -> None:
    """Shows a compact theme selector."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = "Light"

    # Apply current theme
    applyTheme(THEMES[st.session_state["theme"]])

    st.markdown("Choose a Theme")
    st.markdown("---")

    cols = st.columns(len(THEMES))
    for i, theme_name in enumerate(THEMES.keys()):
        with cols[i]:
            is_active = st.session_state["theme"] == theme_name
            theme = THEMES[theme_name]
            # Show a color preview swatch
            st.html(
                f"""
                <div style="
                    background-color: {theme['backgroundColor']};
                    border: 2px solid {'#FF4B4B' if is_active else theme['borderColor']};
                    border-radius: 8px;
                    padding: 8px;
                    text-align: center;
                    margin-bottom: 8px;
                ">
                    <div style="
                        background-color: {theme['primaryColor']};
                        height: 20px;
                        border-radius: 4px;
                        margin-bottom: 4px;
                    "></div>
                    <div style="
                        background-color: {theme['secondaryBackgroundColor']};
                        height: 20px;
                        border-radius: 4px;
                    "></div>
                </div>
                """,
            )
            if st.button(
                f"{'✓ ' if is_active else ''}{theme_name}",
                key=f"theme_btn_{theme_name}",
                width='stretch',
            ):
                st.session_state["theme"] = theme_name
                st.rerun()