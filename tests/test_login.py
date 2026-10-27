import pytest
from playwright.async_api import expect
from pages.login_page import LoginPage
from pages.login_dashboard_page import LoginDashboardPage

# Constants declaration
#Main test URL
URL = "https://demo.applitools.com/"


@pytest.fixture(scope="function")
async def login_page(page):
    await page.goto(URL, wait_until="load")
    login_page = LoginPage(page)
    return login_page


@pytest.mark.BAT
async def test_verify_icons(login_page, logger):
    
    await expect(login_page.TWITTER_ICON).to_be_visible()
    await expect(login_page.FACEBOOK_ICON).to_be_visible()
    await expect(login_page.INSTA_ICON).to_be_visible()

    await logger.log(f"Test |{__name__}| passed")


@pytest.mark.BAT
async def test_login(login_page, logger, page):
    print(f'\n------{__name__}------')

    await login_page.enter_username()
    await login_page.enter_password()
    await login_page.check_remember_box()
    await login_page.click_sigin()

    login_dashboard_page = LoginDashboardPage(page);
    await expect(login_dashboard_page.LOGGEDUSERNAME).to_have_text("Jack Gomez")

    await logger.log(f"Test |{__name__}| passed")
