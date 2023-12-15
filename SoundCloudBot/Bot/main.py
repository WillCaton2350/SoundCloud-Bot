from Bot.States.data import gecko_driver_path, url, artist_xpath, user
from Bot.States.data import search_class,first_autoplay_btn_xpath
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
        self.driver.maximize_window()

    def start_browser(self):
        self.driver.get(url)
        print("Browser")
        try:
            WDW(self.driver, 
                timeout=10).until(
            EC.url_matches(url))
        except PageNotFoundError as err:
            print(err)

    def search_bar(self):
        try:
            WDW(self.driver,10).until(
                EC.presence_of_element_located((
                    By.CLASS_NAME,search_class)
            ))
        except NoSuchElementException as err:
            print(err)
        sleep(1)
        self.driver.find_element(
            By.CLASS_NAME,
        search_class).send_keys(user)
        sleep(1)
        self.driver.find_element(
            By.CLASS_NAME,
        search_class).send_keys(Keys.ENTER)
        print('Artist name typed')
        sleep(1)

    def artist(self):
        try:
            WDW(self.driver,10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    artist_xpath
                )))
        except NoSuchElementException as err:
            print(err)
        self.driver.find_element(
            By.XPATH,
        artist_xpath).click()
        print('artist clicked')
        try:
            WDW(
                self.driver,10).until(
                    EC.presence_of_element_located((
                        By.XPATH,first_autoplay_btn_xpath)))
        except NoSuchElementException as err:
            print(err)

    def auto_play(self):
        number = 1
        while number <= 10:
            try:
                WDW(
                    self.driver,10).until(
                        EC.presence_of_element_located((
                            By.XPATH,
                    first_autoplay_btn_xpath
                )))
            except NoSuchElementException as err:
                print(err)
            self.driver.find_element(
                By.XPATH,
            first_autoplay_btn_xpath).click()
            print("song playing")
            sleep(5)
            number +=1
            break


    def close_browser(self):
        self.driver.close()