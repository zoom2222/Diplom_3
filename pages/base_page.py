from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import allure

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.action = ActionChains(driver)

    # Основные методы навигации
    def open_page(self, url):
        self.driver.get(url)

    def get_current_url(self):
        return self.driver.current_url

    def wait_for_url(self, url):
        self.wait.until(EC.url_to_be(url))

    def refresh_page(self):
        self.driver.refresh()

    # Методы работы с элементами
    def find_element(self, locator, by=By.XPATH):
        return self.wait.until(EC.presence_of_element_located((by, locator)))

    def find_elements(self, locator, by=By.XPATH):
        return self.wait.until(EC.presence_of_all_elements_located((by, locator)))

    def is_element_visible(self, locator, by=By.XPATH):
        try:
            return bool(self.wait.until(EC.visibility_of_element_located((by, locator))))
        except:
            return False

    def wait_for_element_to_disappear(self, locator, by=By.XPATH):
        self.wait.until(EC.invisibility_of_element_located((by, locator)))

    # Методы взаимодействия
    def click_element(self, locator, by=By.XPATH):
        element = self.wait.until(EC.element_to_be_clickable((by, locator)))
        element.click()

    def click_element_with_js(self, locator, by=By.XPATH):
        element = self.find_element(locator, by)
        self.driver.execute_script("arguments[0].click();", element)

    def input_text(self, locator, text, by=By.XPATH):
        element = self.wait.until(EC.visibility_of_element_located((by, locator)))
        element.clear()
        element.send_keys(text)

    def get_element_text(self, locator, by=By.XPATH):
        element = self.wait.until(EC.visibility_of_element_located((by, locator)))
        return element.text

    def get_element_attribute(self, locator, attribute, by=By.XPATH):
        element = self.find_element(locator, by)
        return element.get_attribute(attribute)

    # Методы скроллинга
    def scroll_to_element(self, locator, by=By.XPATH):
        element = self.find_element(locator, by)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.wait.until(EC.visibility_of(element))

    def scroll_to_element_center(self, locator, by=By.XPATH):
        element = self.find_element(locator, by)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.wait.until(EC.visibility_of(element))

    # Методы drag-and-drop
    def drag_and_drop(self, source_locator, target_locator, by=By.XPATH):
        source = self.find_element(source_locator, by)
        target = self.find_element(target_locator, by)
        self.action.drag_and_drop(source, target).perform()

    # Методы для работы с окнами
    def switch_to_new_window(self):
        self.wait.until(EC.number_of_windows_to_be(2))
        new_window = self.driver.window_handles[1]
        self.driver.switch_to.window(new_window)

    def close_current_window(self):
        self.driver.close()

    # Методы для скриншотов
    def attach_screenshot(self, name):
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

    def save_screenshot(self, filepath):
        self.driver.save_screenshot(filepath)

    # Дополнительные проверки
    def is_text_present(self, text):
        return text in self.driver.page_source