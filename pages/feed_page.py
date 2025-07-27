from locators.feed_locators import FeedLocators
from pages.base_page import BasePage
import allure

class FeedPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Получить общее количество заказов")
    def get_total_orders_count(self):
        count_text = self.get_element_text(FeedLocators.TOTAL_ORDERS_COUNT)
        return int(count_text)

    @allure.step("Получить количество заказов за сегодня")
    def get_today_orders_count(self):
        count_text = self.get_element_text(FeedLocators.TODAY_ORDERS_COUNT)
        return int(count_text)

    @allure.step("Проверить наличие заказа {order_number} в работе")
    def is_order_in_progress(self, order_number):
        locator = FeedLocators.ORDER_IN_PROGRESS.format(order_number)
        return self.is_element_visible(locator)

    @allure.step("Дождаться изменения счетчика заказов")
    def wait_for_orders_count_change(self, initial_count, timeout=10):
        self.wait.until(
            lambda d: self.get_total_orders_count() > initial_count,
            message=f"Счетчик заказов не изменился за {timeout} секунд"
        )

    @allure.step("Дождаться появления заказа {order_number} в работе")
    def wait_for_order_in_progress(self, order_number, timeout=10):
        self.wait.until(
            lambda d: self.is_order_in_progress(order_number),
            message=f"Заказ {order_number} не появился в работе за {timeout} секунд"
        )