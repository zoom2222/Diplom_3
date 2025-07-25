from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from locators.feed_locators import FeedLocators
from data import Urls


class FeedPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_total_orders_count(self):
        return int(self.driver.find_element(By.XPATH, FeedLocators.TOTAL_ORDERS_COUNT).text)

    def get_today_orders_count(self):
        return int(self.driver.find_element(By.XPATH, FeedLocators.TODAY_ORDERS_COUNT).text)

    def is_order_in_progress(self, order_number):
        try:
            self.driver.find_element(By.XPATH, FeedLocators.ORDER_IN_PROGRESS.format(order_number))
            return True
        except:
            return False

    def get_first_order_number(self):
        order_card = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, FeedLocators.ORDER_CARD))
        )
        return order_card.text.split('\n')[0]