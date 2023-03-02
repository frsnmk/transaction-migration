from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Transaction:

    def __init__(self) -> None:
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 30)
        self.driver.get("http://localhost:8000/login")
        username_el = self.driver.find_element(by=By.NAME, value="username")
        username_el.send_keys("admin")
        password_el = self.driver.find_element(by=By.NAME, value="password")
        password_el.send_keys("password")
        password_el.send_keys(Keys.ENTER)


    def close(self):
        self.driver.close()

