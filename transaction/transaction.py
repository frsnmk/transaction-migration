from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class Transaction:

    def __init__(self) -> None:
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 30)
        self.driver.get('http://localhost:8000')
