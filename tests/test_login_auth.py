import pytest
from playwright.async_api import expect


@pytest.mark.AUTH
async def test_login_with_auth(auth_page, logger_auth):
    print(f'\n------{__name__}------')

    await auth_page.goto("https://myaccount.google.com/")
    expect(auth_page).to_have_title("Cuenta de Google")
    await logger_auth.log(f'Page |{await auth_page.title()}| opened')