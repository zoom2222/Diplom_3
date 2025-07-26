from locators.auth_locators import AuthLocators
from data import Urls
import allure
from pages.base_page import BasePage

class AuthPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Авторизация пользователя с email {email} и паролем {password}")
    def login(self, email, password):
        self.input_text(AuthLocators.EMAIL_INPUT, email)
        self.input_text(AuthLocators.PASSWORD_INPUT, password)
        self.click_element(AuthLocators.LOGIN_BUTTON)
        self.wait_for_url(Urls.CONSTRUCTOR_URL)