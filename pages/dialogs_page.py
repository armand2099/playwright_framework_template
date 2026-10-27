from pages.base_page import BasePage
from playwright.async_api import Page, Dialog

class DialogPage(BasePage):
    '''
    Login Page methods
    '''

    def __init__(self, page: Page):
        '''
        Initialize LoginPage class
        '''
        #Initialize parent class
        super().__init__(page)

        #Get driver fixture
        self.page = page

        #Declare page elements locators
        self.alert_button = self.page.get_by_role('button', name='Show alert box')
        self.alert_text = self.page.locator('.inline-explanation#alertexplanation')
        self.confirm_button = self.page.get_by_role('button', name='Show confirm box')
        self.confirm_text = self.page.locator('.inline-explanation#confirmexplanation')
        self.confirm_return = self.page.locator('p#confirmreturn')
        self.promp_box_button = self.page.get_by_role('button', name='Show prompt box')
        self.promp_return = self.page.locator('p#promptreturn')
        self.prompt_text = self.page.locator('.inline-explanation#promptexplanation')


    async def on_dialog_accept(self, dialog: Dialog, prompt_text: str = ''):
        #Accepts a browser dialog, entering "Hello World!" when it accepts text input.
        print(f'Dialog {dialog.message} Opened')
        await dialog.accept(prompt_text)
        print(f'Dialog {dialog.message} Accepted')


    async def on_dialog_cancel(self, dialog: Dialog):
        #Accepts a browser dialog, entering "Hello World!" when it accepts text input.
        print(f'Dialog {dialog.message} Opened')
        await dialog.dismiss()
        print(f'Dialog {dialog.message} Dismissed')


    async def alert_dialog(self):
        #Opens the alert dialog
        self.page.once('dialog', lambda dialog: self.on_dialog_accept(dialog, ""))
        await self.alert_button.click()
        print('Alert dialog button click')


    async def confirm_dialog(self, confirmed: bool = True, prompt_text: str = ''):
        #Opens the confirm dialog.
        if confirmed:
            self.page.once('dialog', lambda dialog: self.on_dialog_accept(dialog, prompt_text))
            await self.confirm_button.click()
            print('Confirm Dialog button clicked')
        else:
            self.page.once('dialog', self.on_dialog_cancel)
            await self.confirm_button.click()

        print('Confirm Dialog button clicked')

    async def prompt_dialog(self, confirmed: bool = True, prompt_text: str = ''):
        #Opens the prompt dialog
        if confirmed:
            self.page.once('dialog', lambda dialog: self.on_dialog_accept(dialog, prompt_text))
            await self.promp_box_button.click()
        else:
            self.page.once('dialog', self.on_dialog_cancel)
            await self.promp_box_button.click()
        print('Prompt Dialog button clicked')