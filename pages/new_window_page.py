from pages.base_page import BasePage
from playwright.async_api import Page, Locator, BrowserContext

class NewWindowPage (BasePage):
    '''
    NewWindowPage Page methods
    ''' 

    def __init__(self, page: Page, context: BrowserContext):
        '''
        Initialize LoginPage class
        '''
        #Initialize parent class
        super().__init__(page)

        #Get driver fixture
        self.page = page
        self.context = context

        #Declare page elements locators
        self.new_tab_button = self.page.get_by_role('button', name='New Tab')
        self.new_window_button = self.page.get_by_role('button', name='New Window', exact=True)
        self.new_window_msg_button = self.page.get_by_role('button', name='New Window Message')


    async def new_page(self, page_button: Locator) -> Page:
        #Clicks the required button, waits for the new page to load and returns the new tab page object
        retry = 0
        
        while True:
            async with self.context.expect_page() as page_info:
                await self.page.bring_to_front()
                await page_button.click()
            
            retry = +1

            new_tab = await page_info.value
            
            await new_tab.wait_for_load_state()
            await new_tab.wait_for_selector('body')

            if new_tab.is_closed or retry > 5:
                break

        return new_tab