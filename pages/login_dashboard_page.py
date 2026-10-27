from pages.base_page import BasePage
from playwright.async_api import Page

class LoginDashboardPage(BasePage):
    '''
    Initialize LoginDashboardPage class
    '''

    def __init__(self, page: Page):
        #Initialize parent class
        super().__init__(page)

        #Get driver fixture
        self.page = page

        #Declare page elements locators
        self.LOGGEDUSERNAME = self.page.locator('div.logged-user-name')