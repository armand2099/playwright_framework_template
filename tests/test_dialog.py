import pytest
from pages.dialogs_page import DialogPage
from playwright.async_api import Page, async_playwright, expect

DIALOGS_URL = "https://testpages.eviltester.com/pages/basics/alerts-javascript/"

@pytest.fixture(scope="function")
async def dialog_page(page):
    await page.goto(DIALOGS_URL)
    dialog_page = DialogPage(page)
    return dialog_page

@pytest.mark.DIAL
async def test_alert(dialog_page: DialogPage, logger):
    await expect(dialog_page.alert_text).to_contain_text('')
    await dialog_page.alert_dialog()
    await expect(dialog_page.alert_text).to_contain_text('You triggered and handled the alert dialog')
    await logger.log("Alert Dialog")

@pytest.mark.DIAL
async def test_confirm_accept(dialog_page: DialogPage, logger):
    await expect(dialog_page.confirm_text).to_contain_text('')
    await dialog_page.confirm_dialog()
    await expect(dialog_page.confirm_return).to_contain_text('true')
    await expect(dialog_page.confirm_text).to_contain_text('You clicked OK, confirm returned')
    await logger.log("Confirm Dialog: " + await dialog_page.confirm_text.text_content())

@pytest.mark.DIAL
async def test_confirm_dismiss(dialog_page: DialogPage, logger):
    await expect(dialog_page.confirm_text).to_contain_text('')
    await dialog_page.confirm_dialog(False)
    await expect(dialog_page.confirm_return).to_contain_text('false')
    await expect(dialog_page.confirm_text).to_contain_text('You clicked Cancel, confirm returned')
    await logger.log("Dismiss Dialog: " + await dialog_page.confirm_text.text_content())

@pytest.mark.DIAL
async def test_accept_prompt_dialog(dialog_page: DialogPage, logger):
    await expect(dialog_page.prompt_text).to_contain_text('')
    await dialog_page.prompt_dialog(True, 'Hello World!')
    await expect(dialog_page.prompt_text).to_contain_text("You clicked OK. 'prompt' returned")
    await expect(dialog_page.promp_return).to_contain_text('Hello World!')
    await logger.log("Accept Prompt Dialog: " + await dialog_page.promp_return.text_content())

@pytest.mark.DIAL
async def test_dismiss_prompt_dialog(dialog_page: DialogPage, logger):
    await expect(dialog_page.prompt_text).to_contain_text('')
    await dialog_page.prompt_dialog(False)
    await expect(dialog_page.prompt_text).to_contain_text("You clicked Cancel. 'prompt' returned")
    expect(dialog_page.confirm_return).to_be_empty
    await logger.log("Dismiss Prompt Dialog: " + await dialog_page.prompt_text.text_content())