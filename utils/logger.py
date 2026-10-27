import os
from logging import Logger, getLogger
import datetime
import base64
import pytest_html
from playwright.async_api import Page


class Loggin:
    '''
    Sends logs to report
    '''

    def __init__(self, page: Page, extras):
        self.extras = extras
        self.page = page
        self.ss_name = f"report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
        self.ss_path = os.path.join(os.getcwd(), "Reports", "screenshots", self.ss_name)

    async def take_screenshot(self) -> str:
        '''
        Takes a page screenshot
        '''
        screenshot = await self.page.screenshot()
        return base64.b64encode(screenshot).decode("ascii")

    def message(self, message: str, stacklevel: int = 2) -> Logger:
        '''
        Adds message to HTML report
        '''
        logger = getLogger()
         
        # pytest captures this logger for both the report and console output.
        logger.info(message, stacklevel=stacklevel)
        print(message)

        return logger
    
    async def log(self, message: str) -> None:
        '''
        Sends message to the report file and console.
        Takes a screenshot of the current browser when report extras are enabled.
        '''
        #logger = logging.getLogger(__name__)

        # pytest captures this logger for both the report and console output.
        #logger.info(message, stacklevel=1)

        logger = self.message(message, 3)

        if self.extras is not None:
            try:
                screenshot = await self.take_screenshot()
            except Exception as error:
                logger.warning(f"Unable to attach screenshot: {error}", stacklevel=3)
            else:
                self.extras.append(
                    pytest_html.extras.image(
                        screenshot,
                        mime_type="image/png",
                        name="Screenshot",
                    )
                )
