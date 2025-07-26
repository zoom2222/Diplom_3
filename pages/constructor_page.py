from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from locators.constructor_locators import ConstructorLocators
from data import Urls
import allure
import pytest

class ConstructorPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Кликнуть на вкладку 'Конструктор'")
    def click_constructor_tab(self):
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, ConstructorLocators.CONSTRUCTOR_TAB)))
        self.driver.execute_script("arguments[0].click();", element)
        self.wait.until(EC.url_to_be(Urls.CONSTRUCTOR_URL))

    @allure.step("Кликнуть на вкладку 'Лента заказов'")
    def click_feed_tab(self):
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, ConstructorLocators.FEED_TAB)))
        self.driver.execute_script("arguments[0].click();", element)
        self.wait.until(EC.url_to_be(Urls.FEED_URL))

    @allure.step("Кликнуть на ингредиент {ingredient_name}")
    def click_ingredient(self, ingredient_name):
        try:
            # Прокручиваем к разделу булок
            buns_header = self.wait.until(
                EC.presence_of_element_located((By.XPATH,
                    ConstructorLocators.BUNS_SECTION + "/preceding-sibling::h2")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", buns_header)

            locator = ConstructorLocators.INGREDIENT_ITEM.format(ingredient_name)
            element = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, locator)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            self.wait.until(EC.visibility_of(element))
            element.click()
        except Exception as e:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=f"ingredient_error_{ingredient_name}",
                attachment_type=allure.attachment_type.PNG
            )
            pytest.fail(f"Не удалось кликнуть на ингредиент {ingredient_name}: {str(e)}")

    @allure.step("Проверить видимость модального окна с деталями ингредиента")
    def is_ingredient_details_visible(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, ConstructorLocators.INGREDIENT_DETAILS_MODAL)))
        except:
            return False

    @allure.step("Добавить ингредиент {ingredient_name} в заказ")
    def add_ingredient_to_order(self, ingredient_name):
        locator = ConstructorLocators.INGREDIENT_ITEM.format(ingredient_name)
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, locator)))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        source = self.driver.find_element(By.XPATH, locator)
        target = self.driver.find_element(By.XPATH, ConstructorLocators.ORDER_BUTTON + "/..")
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    @allure.step("Получить счетчик для ингредиента {ingredient_name}")
    def get_ingredient_counter(self, ingredient_name):
        locator = ConstructorLocators.INGREDIENT_COUNTER.format(ingredient_name)
        try:
            counter = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, locator)))
            return int(counter.text) if counter.text else 0
        except:
            return 0

    @allure.step("Сделать заказ")
    def make_order(self):
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, ConstructorLocators.ORDER_BUTTON))).click()

    @allure.step("Получить номер заказа")
    def get_order_number(self):
        order_number = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ConstructorLocators.ORDER_MODAL)))
        return order_number.text

    @allure.step("Закрыть модальное окно")
    def close_modal(self):
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, ConstructorLocators.MODAL_CLOSE_BUTTON))).click()
        self.wait.until(EC.invisibility_of_element_located(
            (By.XPATH, ConstructorLocators.INGREDIENT_DETAILS_MODAL)))