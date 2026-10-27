import pytest
from utils.rest import Rest
from playwright.async_api import async_playwright

#API test URL
API_URL = "https://api.duckduckgo.com/"


@pytest.mark.API
async def test_api(logger):

    rest_client = Rest(API_URL)
    async with async_playwright() as p:
        response = await rest_client.rest_get(p, "Playwright")
        assert response.status == 200
        logger.message(f"Status Code: {response.status}")

        header = (await response.json())['Heading'].lower()
        assert header == "playwright"
        logger.message(f"Header: {header}")