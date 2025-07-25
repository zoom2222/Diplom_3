from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from locators.auth_locators import AuthLocators
from data import Urls

class AuthPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def login(self, email, password):
        self.driver.find_element(By.CSS_SELECTOR, AuthLocators.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(By.CSS_SELECTOR, AuthLocators.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, AuthLocators.LOGIN_BUTTON).click()
        self.wait.until(EC.url_to_be(Urls.CONSTRUCTOR_URL))