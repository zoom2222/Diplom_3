from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from locators.constructor_locators import ConstructorLocators
from data import Urls

class ConstructorPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def click_constructor_tab(self):
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, ConstructorLocators.CONSTRUCTOR_TAB)))
        self.driver.execute_script("arguments[0].click();", element)
        self.wait.until(EC.url_to_be(Urls.CONSTRUCTOR_URL))

    def click_feed_tab(self):
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, ConstructorLocators.FEED_TAB)))
        self.driver.execute_script("arguments[0].click();", element)
        self.wait.until(EC.url_to_be(Urls.FEED_URL))

    def click_ingredient(self, ingredient_name):
        try:
            # Прокручиваем к разделу булок
            buns_header = self.wait.until(
                EC.presence_of_element_located((By.XPATH, ConstructorLocators.BUNS_SECTION + "/preceding-sibling::h2")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", buns_header)

            locator = ConstructorLocators.INGREDIENT_ITEM.format(ingredient_name)
            element = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, locator)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)  # Небольшая пауза для стабилизации
            element.click()
        except Exception as e:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=f"ingredient_error_{ingredient_name}",
                attachment_type=allure.attachment_type.PNG
            )
            pytest.fail(f"Не удалось кликнуть на ингредиент {ingredient_name}: {str(e)}")

    def is_ingredient_details_visible(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, ConstructorLocators.INGREDIENT_DETAILS_MODAL)))
        except:
            return False

    def add_ingredient_to_order(self, ingredient_name):
        locator = ConstructorLocators.INGREDIENT_ITEM.format(ingredient_name)
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, locator)))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        source = self.driver.find_element(By.XPATH, locator)
        target = self.driver.find_element(By.XPATH, "//div[contains(@class, 'BurgerConstructor_basket')]")
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    def get_ingredient_counter(self, ingredient_name):
        locator = ConstructorLocators.INGREDIENT_COUNTER.format(ingredient_name)
        try:
            counter = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, locator)))
            return int(counter.text) if counter.text else 0
        except:
            return 0

    def make_order(self):
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, ConstructorLocators.ORDER_BUTTON))).click()

    def get_order_number(self):
        order_number = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ConstructorLocators.ORDER_MODAL)))
        return order_number.text

    def close_modal(self):
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, ConstructorLocators.MODAL_CLOSE_BUTTON))).click()
        self.wait.until(EC.invisibility_of_element_located(
            (By.XPATH, ConstructorLocators.INGREDIENT_DETAILS_MODAL)))
