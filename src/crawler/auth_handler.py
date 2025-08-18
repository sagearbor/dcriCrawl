"""Authentication handler for manual login using Playwright."""
from pathlib import Path
from playwright.sync_api import sync_playwright

class AuthHandler:
    """Handles manual authentication and stores session state."""

    def __init__(self, storage_path: str = "data/auth_state.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def login(self, url: str) -> None:
        """Open a browser for the user to log in manually.

        The authenticated state is saved to ``self.storage_path`` so that
        subsequent runs can re-use the login session."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(url)
            print("Please complete login in the opened browser window...")
            page.wait_for_timeout(30000)  # wait 30s for manual login
            context.storage_state(path=str(self.storage_path))
            browser.close()
