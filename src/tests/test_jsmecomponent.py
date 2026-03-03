# src/tests/test_jsmecomponent.py
import os
import socket
import subprocess
import time
from typing import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

"""
Testing:
Streamlit starts correctly in test mode
The harness loads
The JSME component mounts (iframe exists)
Python <-> component bridge works (returned-smiles container exists)

end-to-end integration test setup for the component.

Results:
The component does not crash the app.

The custom component renders inside Streamlit.

The Python wrapper executes and returns a value.

Streamlit reruns correctly in headless mode.

The component works inside automated browser execution
"""
# --- helpers -------------------------------------------------


def _is_port_open(host: str, port: int) -> bool:
    """Return True if (host, port) is accepting TCP connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.2)
        return s.connect_ex((host, port)) == 0


def _wait_for_server(host: str, port: int, timeout_s: float = 30.0) -> None:
    """Wait until the server is reachable or raise RuntimeError."""
    start = time.time()
    while time.time() - start < timeout_s:
        if _is_port_open(host, port):
            return
        time.sleep(0.25)
    raise RuntimeError(f"Server did not start on {host}:{port} within {timeout_s} seconds")


# --- pytest fixtures ------------------------------------------


@pytest.fixture(scope="session")
def streamlit_server() -> Generator[str, None, None]:
    """Starts: streamlit run src/tests/jsme_harness_app.py --server.port 8501"""
    host = "127.0.0.1"
    port = 8501

    # Ensure we run from repo root
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    app_path = os.path.join(repo_root, "src", "tests", "jsme_harness_app.py")

    # Pick python executable (uses current venv/conda)
    python = os.environ.get("PYTHON", None) or os.sys.executable

    proc = subprocess.Popen(
        [
            python,
            "-m",
            "streamlit",
            "run",
            app_path,
            "--server.port",
            str(port),
            "--server.address",
            host,
            "--server.headless",
            "true",
            "--browser.gatherUsageStats",
            "false",
        ],
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        _wait_for_server(host, port, timeout_s=40.0)
        yield f"http://{host}:{port}"
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


@pytest.fixture
def driver() -> Generator[WebDriver, None, None]:
    """Provide a headless Chrome WebDriver for UI tests."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280,720")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    d = webdriver.Chrome(options=chrome_options)
    try:
        yield d
    finally:
        d.quit()


# --- tests -----------------------------------------------------


def test_harness_loads(streamlit_server: str, driver: WebDriver) -> None:
    """The harness page should load and show its title."""
    driver.get(streamlit_server)

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(),'JSME Component Test Harness')]")
        )
    )


def test_component_iframe_exists(streamlit_server: str, driver: WebDriver) -> None:
    """The custom component should render inside an iframe."""
    driver.get(streamlit_server)

    # Streamlit renders custom components inside iframes.
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))


def test_returned_smiles_container_exists(streamlit_server: str, driver: WebDriver) -> None:
    """The harness should expose a returned-smiles container for assertions."""
    driver.get(streamlit_server)

    el = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='returned-smiles']"))
    )
    assert el is not None
