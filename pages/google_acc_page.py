from pages.base_page import BasePage
from playwright.async_api import Page

class GoogleAccPage(BasePage):
    '''
    Login Page methods
    '''

    def __init__(self, page: Page):
        '''
        Initialize GoogleAccPage class
        '''
        #Initialize parent class
        super().__init__(page)

        #Get driver fixture
        self.page = page

        #Declare page elements locators
        self.email = self.page.get_by_label("Email or phone")
        self.nextButton = self.page.get_by_text("Next")
        self.password = self.page.get_by_label("Enter your password")


    async def enter_email(self, email: str):
        #Enter email
        await self.email.fill(email)

    async def enter_password(self, password: str):
        #Enter password
        await self.password.fill(password)

    async def click_next_button(self):
        #Click next button
        await self.nextButton.click()