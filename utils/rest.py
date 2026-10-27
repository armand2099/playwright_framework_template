import asyncio
import random
from playwright.async_api import Error, Playwright


class Rest:
    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }


    def __init__(self, api_url: str):
        self.API_URL = api_url


    async def api_context(self, playwright: Playwright):
        return await playwright.request.new_context(
            base_url=self.API_URL,
            extra_http_headers=self.HEADERS
        )

    async def rest_get(self, playwright: Playwright, body: str):
        context = await self.api_context(playwright)
        try:
            await asyncio.sleep(random.uniform(1.5, 3.0))
            params = {"q": body, "format": "json"}
            response = await context.get("/", params=params, timeout=10000)
            return response
            
        except Error as e:
            print(f"Playwright error while making GET request: {e}")
            raise

    
    async def rest_find(self, body: list, phrase: str):
        '''
        Searches a phrase in the rest response
        '''
        response = (await body.json())['Heading'].lower()
        assert phrase.lower() == response


    async def rest_response_code(self, body: list, code: int):
        '''
        Validates response status code
        '''
        assert (body.status_code) == code