import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.common.exceptions import NoSuchElementException
from urllib.error import HTTPError as PageNotFoundError
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver as web
from datetime import datetime
from time import sleep
from PyQt6.QtGui import QPixmap
from PIL import Image, ImageQt
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# STATES
gecko_driver_path = 'Driver/geckodriver'
url = 'https://soundcloud.com/'
specific_url = 'https://soundcloud.com/willcatonjr/what-you-doing-tonight-ft-kurtiz-the-kid'
login_btn_xpath = '/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div/div/2/button[1]'
user_xpath = '//*[@id="sign_in_up_email"]'
search_class = 'headerSearch__input'
password_xpath = '//*[@id="enter_password_field"]'
user = "WillCatonJr"
first_autoplay_btn_xpath = '/html/body/div[2]/div[2]/div[2]/div/div[4]/div[1]/div/div[2]/div/div[2]/ul/li[1]/div/div/div/div[2]/div[1]/div/div/div[1]/a'
artist_xpath = '/html/body/div[2]/div[2]/div[2]/div/div/div[3]/div/div/div/ul/li[1]/div/div/div/h2/a'
auto_play_btn = '/html/body/div[2]/div[2]/div[2]/div/div/div[3]/div/div/div/ul/li[2]/div/div/div/div[2]/div[1]/div/div/div[1]/a'
search_bar_xpath = '/html/body/div[3]/div[2]/div[2]/div/div/div[2]/div/div[1]/span/span/form/input'
target_autoplay_xpath = '/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/a'

# BEHAVIORS
class web_driver:
    def __init__(self):
        self.driver = None

    def start_driver(self):
        print("Start Browser")
        firefox_options = web.FirefoxOptions()
        os.environ["webdriver.firefox.driver"] = gecko_driver_path
        self.driver = web.Firefox(options=firefox_options)
        self.driver.minimize_window()

    def start_browser(self):
        self.driver.get(url)
        print("Browser")
        try:
            WDW(self.driver, timeout=10).until(
                EC.url_matches(url))
        except PageNotFoundError as err:
            print(err)

    def search_bar(self):
        try:
            WDW(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.CLASS_NAME, search_class)
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
            WDW(self.driver, 10).until(
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
                self.driver, 10).until(
                    EC.presence_of_element_located((
                        By.XPATH, first_autoplay_btn_xpath)))
        except NoSuchElementException as err:
            print(err)

    def auto_play(self):
        try:
            WDW(
                self.driver, 10).until(
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
        sleep(2)

    def close_browser(self):
        self.driver.quit()

class SimpleGUI(QWidget):
    def __init__(self, selenium_script):
        super().__init__()
        self.selenium_script = selenium_script
        self.func = None 
        self.init_ui()

    def init_ui(self):
        image_path = '/Users/administrator/Desktop/Projects/exe_file/img/logo.png'
        pillow_image = Image.open(image_path)
        q_image = ImageQt.ImageQt(pillow_image)
        pixmap = QPixmap.fromImage(q_image)

        self.logo = QLabel(self)
        self.logo.setPixmap(pixmap)

        self.start_button = QPushButton('Start', self)
        button_style = '''
            QPushButton {
                background-color: #141414; /* Your desired color */
                color: white; /* Text color */
            }
        '''
        self.start_button.setStyleSheet(button_style)
        self.start_button.clicked.connect(self.start_selenium_loop)
        layout = QVBoxLayout()
        layout.addWidget(self.logo)
        layout.addWidget(self.start_button)
        self.setLayout(layout)
        self.setFixedSize(340, 400)
        self.setWindowTitle('SoundCloud Bot')

        gradient_style = '''
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #fe8c00, stop:1 #f83600);
        '''
        self.setStyleSheet(gradient_style)

    def start_selenium_loop(self):
        counter = 100
        self.func = web_driver()
        start_time = datetime.now()
        print(f'Start Time: {start_time.strftime("%H:%M:%S")}')
        for i in range(counter):
            self.func.start_driver()
            self.func.start_browser()
            self.func.search_bar()
            self.func.artist()
            self.func.auto_play()
            elapsed_time = datetime.now() - start_time
            formatted_time = str(elapsed_time).split(".")[0]
            print(f'Elapsed Time: {formatted_time}, Plays: {counter}\n')
            counter += 1
            self.func.close_browser()
        end_time = datetime.now()
        print(f'End Time: {end_time.strftime("%H:%M:%S")}')
        self.func.close_browser()

    def start_selenium(self):
        subprocess.run(["python", self.selenium_script])
        print('Selenium script started.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    selenium_script_path = "soundcloudbot.py"
    window = SimpleGUI(selenium_script_path)
    window.show()
    sys.exit(app.exec())
