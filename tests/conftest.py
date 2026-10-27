import pytest
import os
import datetime
from pages.google_acc_page import GoogleAccPage
import auth.google_creds as creds
from utils.logger import Loggin
from pathlib import Path
from playwright.async_api import Browser, async_playwright, Playwright, Page

#Variable declaration
HEADLESS = False
image_name = f"report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
file_name = os.path.join(os.getcwd(), "Reports", "screenshots", image_name)

#-----------------------------------------Multiple browsers implementation-----------------------------------------
# Browser Factory
class BrowserFactory:
    @staticmethod
    async def get_browser(playwright: Playwright, browser_name: str, headless: bool = False) -> Browser:
        '''Lauches browser dinamically'''
        browsers = {
            "chromium": playwright.chromium,
            "firefox": playwright.firefox,
            "webkit": playwright.webkit
        }
        
        target_browser = browsers.get(browser_name.lower())
        if not target_browser:
            raise ValueError(f"Unsupported browser type: '{browser_name}'. Choose chromium, firefox, or webkit.")
            
        if browser_name.lower() == 'firefox':
            return await target_browser.launch(headless=headless, slow_mo=500, args=["--width=1280", "--height=720", "--disable-blink-features=AutomationControlled"])
        else:
            return await target_browser.launch(headless=headless, slow_mo=500, args=["--start-maximized", "--disable-blink-features=AutomationControlled"])


# Add custom command-line argument to pytest
def pytest_addoption(parser):
    '''Declares cli argument'''
    parser.addoption(
        "--browser-type", 
        action="store", 
        default="chromium", 
        help="Browser type to run tests on: chromium, firefox, or webkit"
    )


@pytest.fixture(scope="session")
def selected_browser_name(request) -> str:
    """Gets the browser type from the command line."""
    return request.config.getoption("--browser-type")


@pytest.fixture(scope="session")
async def page(selected_browser_name: str):
    """
    Factory-driven fixture.
    """
    # Start the playwright driver context
    async with async_playwright() as p:
        # Use the Factory to get the correct browser dynamically
        browser = await BrowserFactory.get_browser(p, selected_browser_name, headless=HEADLESS)
        print(f"Browser: {selected_browser_name}")
        
        context = await browser.new_context(no_viewport=True)
        page = await context.new_page()
        
        # Give the page to the test function
        yield page
        
        # Safely close resources after the test completes
        await page.screenshot(path=file_name)
        await page.close()
        await context.close()
        await browser.close()


# Session authentication
@pytest.fixture(scope="session")
async def browser(selected_browser_name):
    '''Creates browser object dinamically'''
    async with async_playwright() as p:
        browser = await BrowserFactory.get_browser(p, selected_browser_name, headless=HEADLESS)
        yield browser
        await browser.close()


#-----------------------------------------Multiple browsers implementation-----------------------------------------


#-------------------------------------------Authentication state session-------------------------------------------
# Create the session-scoped authentication state
@pytest.fixture(scope="function")
async def authenticated_state(browser: Browser):
    '''Authenticates and stores authentication state'''
    state_file = Path("auth/state.json").resolve()
    if state_file.is_file():
        # Create a temporary context and page to execute login
        context = await browser.new_context(no_viewport=True, storage_state="auth/state.json")
    else:
        context = await browser.new_context(no_viewport=True)

    page = await context.new_page()

    await page.goto("https://accounts.google.com/")

    google_acc_page = GoogleAccPage(page)

    if await page.title() == "Sign in - Google Accounts":
        await google_acc_page.enter_email(creds.EMAIL)
        await google_acc_page.click_next_button()
        await google_acc_page.enter_password(creds.PASSWORD)
        await google_acc_page.click_next_button()
    
        # Wait for navigation or a specific selector to confirm successful login
        await page.wait_for_url("https://myaccount.google.com/**")
        
        # Save storage state to an in-memory dictionary (or a file string)    
        state = await context.storage_state(path="auth/state.json")
    else:
        state = await context.storage_state()

    await context.close()

    yield state

    await page.screenshot(path=file_name)
    await page.close()


@pytest.fixture(scope="function")
async def auth_page(browser: Browser, authenticated_state):
    '''Loads session state'''
    # Pass the session state directly into the new context
    context = await browser.new_context(no_viewport=True, storage_state=authenticated_state)
    page = await context.new_page()
    
    yield page

    await page.screenshot(path=file_name)
    await context.close()
    await page.close()


#-------------------------------------------Authentication state session-------------------------------------------


#-------------------------------------------Report Fixtures-------------------------------------------
#Logger fixture
@pytest.fixture(scope="function")
def logger(page, extras):
    '''Logs messages and screenshots to html report'''
    return Loggin(page, extras)

#Logger fixture for authenticated session
@pytest.fixture(scope="function")
def logger_auth(auth_page, extras):
    '''Logs messages and screenshots to html report'''
    return Loggin(auth_page, extras)


@pytest.hookimpl (hookwrapper=True)
def pytest_runtest_makereport (item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr (report, "extra", [])
    xfail = False
    if report.when == "call" or report.when == 'setup':
        xfail = hasattr(report, "wasxfail")
    if (report.skipped and xfail) or (report.failed and not xfail):
        # add the screenshots to the html report
        extra.append(pytest_html.extras.png(file_name))
    report.extra = extra