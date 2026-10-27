import time
from playwright.async_api import Error, Locator, Page


class BasePage:
    '''
    Class containing functions common to the whole project
    '''
    # Constants declaration

    def __init__(self, browser: Page):
        '''
        Initialize the browser and navigates to the project page
        The url parameter can be overide
        '''
        self.browser = browser


    async def wait_element(self, element: Locator, timeout: int = 10, state: str = "visible"):
        '''
        Waits for an element to be visible
        '''
        try:
            await element.wait_for(state=state, timeout=timeout * 1000)
            await element.scroll_into_view_if_needed() #Scrolls to the element if it is not visible
            print(f"Element [{await element.get_attribute('id')}] is {state}")
        
        except Error as e:
            print(f"Playwright error while waiting for element: {e}")
            raise

    async def get_page_title(self) -> str:
        '''
        Returns the current page tittle
        '''
        await self.browser.wait_for_load_state('load') #Waits for the page to load before getting the title
        page_title = await self.browser.title()
        print(f"Current page title is: {page_title}")

        return page_title


    async def get_page_url(self) -> str:
        '''
        Returns the current page URL
        '''
        await self.browser.wait_for_load_state('load') #Waits for the page to load before getting the URL
        page_url = await self.browser.url
        print(f"Current page URL is: {page_url}")

        return page_url


    async def click_element(self, element: Locator) -> None:
        '''
        Clicks on an element
        '''
        try:
            name = await element.get_attribute('id')

            await self.wait_element(element) #Waits for the element to be visible
            await element.click()        

            print(f"Clicked on element: {name}") 
        except Error as e:
            print(f"Playwright error while clicking element: {e}")
            raise


    async def fill_element(self, element: Locator, text: str) -> None:
        '''
        Fills an element with the provided text
        '''
        try:
            await self.wait_element(element) #Waits for the element to be visible
            await element.fill(text) #Fills the element with the text

            print(f"Filled element: [{await element.get_attribute('id')}] with text: {text}")
        except Error as e:
            print(f"Playwright error while filling element: {e}")
            raise