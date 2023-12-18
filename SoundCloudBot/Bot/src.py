from Bot.States.data import gecko_driver_path, url, target_autoplay_xpath, user
from Bot.States.data import specific_url,first_autoplay_btn_xpath
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait as WDW 
from selenium.common.exceptions import NoSuchElementException
from urllib.error import HTTPError as PageNotFoundError
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver as web
from time import sleep
import os

class web_driver:
    def __init__(self):
        self.driver = None

    def start_driver(self):
        print("Start Browser")
        firefox_options = web.FirefoxOptions()
        os.environ[
            "webdriver.firefox.driver"
            ] =  gecko_driver_path
        self.driver = web.Firefox(
            options=firefox_options        
        )
        self.driver.minimize_window()

    def start_browser(self):
        self.driver.get(specific_url)
        print("Browser")
        try:
            WDW(self.driver, 
                timeout=10).until(
            EC.url_matches(specific_url))
        except PageNotFoundError as err:
            print(err)

    

    def auto_play(self):
        try:
            WDW(
                self.driver,10).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                target_autoplay_xpath
            )))
        except NoSuchElementException as err:
            print(err)
        self.driver.find_element(
            By.XPATH,
        target_autoplay_xpath).click()
        print("song playing")
        sleep(3)


    def close_browser(self):
        self.driver.close()