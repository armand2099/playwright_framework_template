from pages.base_page import BasePage
from playwright.async_api import Page
import auth.creds as creds


class LoginPage(BasePage):
    '''
    Login Page methods
    '''

    # Constants declaration
    USERNAME = creds.USERNAME
    PASSWORD = creds.PASSWORD


    def __init__(self, page: Page):
        '''
        Initialize LoginPage class
        '''
        #Initialize parent class
        super().__init__(page)

        #Get driver fixture
        self.page = page

        #Declare page elements locators
        self.FORM_NAME =  page.get_by_text("Login Form")
        self.USERNAME = page.get_by_placeholder("Enter your username")
        self.PASSWORD = page.get_by_placeholder("Enter your password")
        self.SIGNIN_BTN = page.get_by_text("Sign In")
        self.REMEMBER_BOX = page.get_by_label("Remember Me")
        self.TWITTER_ICON = page.locator('img[src="img/social-icons/twitter.png"]')
        self.FACEBOOK_ICON = page.locator('img[src="img/social-icons/facebook.png"]')
        self.INSTA_ICON = page.locator('img[src="img/social-icons/linkedin.png"]')
                                       

    async def enter_username(self, username = USERNAME):
        '''
        Fills Login page Username textbox
        '''
        await self.fill_element(self.USERNAME, username)

    async def enter_password(self, password = PASSWORD):
        '''
        Fills Login page Password textbox
        '''
        await self.fill_element(self.PASSWORD, password)

    async def check_remember_box(self):
        '''
        Checks the Remember Me Box
        '''
        if not await self.REMEMBER_BOX.is_checked():
            await self.click_element(self.REMEMBER_BOX)
        else:
            await self.clickElement(self.REMEMBER_BOX)

        print(f"Checkbox {await self.REMEMBER_BOX.get_attribute('id')} checked")

    async def click_sigin(self):
        '''
        Clicks the Singn In button
        '''
        await self.click_element(self.SIGNIN_BTN)
        await self.page.wait_for_load_state('load')