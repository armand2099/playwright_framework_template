import pytest
from utils.logger import Loggin
from pages.new_window_page import NewWindowPage
from playwright.async_api import Page, async_playwright, expect

WINDOWS_URL = "https://demoqa.com/browser-windows"
WINDOWSTEXT = "Knowledge increases by sharing but not by saving. Please share this website with your friends and in your organization."

@pytest.fixture(scope="session")
async def new_windows_page(page):

    await page.goto(WINDOWS_URL, wait_until='load')
    new_window_page = NewWindowPage(page, page.context)
    
    return new_window_page

@pytest.mark.TAB
async def test_new_tab(new_windows_page: NewWindowPage, logger):
    new_tab = await new_windows_page.new_page(new_windows_page.new_tab_button)
    new_tab_header = new_tab.locator('#sampleHeading')
    await expect(new_tab_header).to_contain_text('This is a sample page')
    await logger.log("New Tab opened: " + await new_tab_header.text_content())

@pytest.mark.TAB
async def test_new_window(new_windows_page: NewWindowPage, logger):
    new_window = await new_windows_page.new_page(new_windows_page.new_window_button)
    new_window_header =  new_window.locator('#sampleHeading')
    await expect(new_window_header).to_contain_text('This is a sample page')
    await logger.log("New Window opened: " + await new_window_header.text_content())

@pytest.mark.TAB
async def test_new_window_message(new_windows_page: NewWindowPage, logger):
    new_window_msg = await new_windows_page.new_page(new_windows_page.new_window_msg_button)
    new_window_msg_body =  new_window_msg.locator('body')
    await expect(new_window_msg_body).to_contain_text(WINDOWSTEXT)
    await logger.log("New Window opened: " + await new_window_msg_body.text_content())

@pytest.mark.TAB
async def test_open_tabs_manually(page, extras):
    context = page.context

    tab1 = await context.new_page()
    logger1 = Loggin(tab1, extras)

    tab2 = await context.new_page()
    logger2 = Loggin(tab2, extras)

    await tab1.goto('https://google.com')
    await tab1.wait_for_load_state()
    await logger1.log("Page |" + await tab1.title() + " | Opened")

    await tab2.goto('https://playwright.dev')
    await tab2.wait_for_load_state()
    await logger2.log("Page |" + await tab2.title() + " | Opened")

    await tab1.bring_to_front()
    await tab1.locator('[name="q"]').fill('Playwright')
    await tab1.locator('[name="q"]').press("Enter")
    await logger1.log("Search completed")

    await tab2.bring_to_front()
    await expect(tab2).to_have_title("Fast and reliable end-to-end testing for modern web apps | Playwright")
    await logger2.log("Title validated")