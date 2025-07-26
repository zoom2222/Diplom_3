import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.constructor_page import ConstructorPage
from pages.feed_page import FeedPage
from data import BurgerIngredients, Urls


@allure.feature('Лента заказов')
class TestFeed:
    @allure.story('Навигация')
    @allure.title('Переход в ленту заказов')
    def test_navigate_to_feed(self, driver):
        constructor_page = ConstructorPage(driver)
        constructor_page.click_feed_tab()
        assert driver.current_url == Urls.FEED_URL

    @allure.story('Статистика')
    @allure.title('Проверка счетчиков заказов')
    def test_order_counters_increase(self, driver, login):
        feed_page = FeedPage(driver)
        constructor_page = ConstructorPage(driver)
        wait = WebDriverWait(driver, 10)

        # Получаем начальные значения счетчиков
        initial_total = feed_page.get_total_orders_count()
        initial_today = feed_page.get_today_orders_count()

        # Создаем заказ
        for ingredient in [BurgerIngredients.BUNS[0], BurgerIngredients.FILLINGS[0]]:
            section_locator = f"//h2[text()='{'Булки' if ingredient in BurgerIngredients.BUNS else 'Начинки'}']"
            section = wait.until(
                EC.presence_of_element_located((By.XPATH, section_locator)))
            driver.execute_script("arguments[0].scrollIntoView(true);", section)
            wait.until(EC.visibility_of(section))  # Ждем пока раздел станет видимым
            constructor_page.add_ingredient_to_order(ingredient)

        constructor_page.make_order()
        order_number = constructor_page.get_order_number()
        constructor_page.close_modal()

        # Переходим в ленту заказов
        constructor_page.click_feed_tab()
        wait.until(lambda d: feed_page.get_total_orders_count() > initial_total)  # Ждем обновления счетчиков

        # Проверяем счетчики
        assert feed_page.get_total_orders_count() > initial_total
        assert feed_page.get_today_orders_count() > initial_today

    @allure.story('Статусы')
    @allure.title('Проверка отображения заказа в работе')
    def test_order_in_progress(self, driver, login):
        feed_page = FeedPage(driver)
        constructor_page = ConstructorPage(driver)
        wait = WebDriverWait(driver, 10)

        # Создаем заказ
        for ingredient in [BurgerIngredients.BUNS[0], BurgerIngredients.FILLINGS[0]]:
            section_locator = f"//h2[text()='{'Булки' if ingredient in BurgerIngredients.BUNS else 'Начинки'}']"
            section = wait.until(
                EC.presence_of_element_located((By.XPATH, section_locator)))
            driver.execute_script("arguments[0].scrollIntoView(true);", section)
            wait.until(EC.visibility_of(section))  # Ждем пока раздел станет видимым
            constructor_page.add_ingredient_to_order(ingredient)

        constructor_page.make_order()
        order_number = constructor_page.get_order_number()
        constructor_page.close_modal()

        # Переходим в ленту заказов
        constructor_page.click_feed_tab()
        wait.until(lambda d: feed_page.is_order_in_progress(order_number))  # Ждем появления заказа

        # Проверяем отображение заказа
        assert feed_page.is_order_in_progress(order_number)