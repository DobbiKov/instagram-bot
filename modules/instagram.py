from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from config import FIREFOX_DRIVER_PATH

import time, random

class Instagram:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Firefox(executable_path=FIREFOX_DRIVER_PATH)

    def login(self):
        try:
            self.browser.get(url="https://www.instagram.com")
            time.sleep(random.randrange(3, 5))
            
            username_input = self.browser.find_element_by_name("username")
            username_input.clear()
            username_input.send_keys(self.username)

            time.sleep(random.randrange(3, 5))

            password_input = self.browser.find_element_by_name("password")
            password_input.clear()
            password_input.send_keys(self.password)

            password_input.send_keys(Keys.ENTER)
        except Exception as ex:
            self.finish()

    def finish(self):
        time.sleep(random.randrange(3, 5))
        self.browser.close()
        self.browser.quit()
