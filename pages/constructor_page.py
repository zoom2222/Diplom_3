from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import allure

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def click_element(self, locator):
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, locator)))
        element.click()

    def click_element_with_js(self, locator):
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, locator)))
        self.driver.execute_script("arguments[0].click();", element)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located((By.XPATH, locator)))

    def scroll_to_element(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.wait.until(EC.visibility_of(element))

    def scroll_to_element_center(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.wait.until(EC.visibility_of(element))

    def is_element_visible(self, locator):
        try:
            return bool(self.wait.until(EC.visibility_of_element_located((By.XPATH, locator))))
        except:
            return False

    def wait_for_element_to_disappear(self, locator):
        self.wait.until(EC.invisibility_of_element_located((By.XPATH, locator)))

    def get_element_text(self, locator):
        element = self.wait.until(EC.visibility_of_element_located((By.XPATH, locator)))
        return element.text

    def wait_for_url(self, url):
        self.wait.until(EC.url_to_be(url))

    def attach_screenshot(self, name):
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )