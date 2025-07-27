import pytest
import allure
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
        assert constructor_page.get_current_url() == Urls.FEED_URL

    @allure.story('Статистика')
    @allure.title('Проверка счетчиков заказов')
    def test_order_counters_increase(self, driver, login):
        feed_page = FeedPage(driver)
        constructor_page = ConstructorPage(driver)

        # Получаем начальные значения счетчиков
        initial_total = feed_page.get_total_orders_count()
        initial_today = feed_page.get_today_orders_count()

        # Создаем заказ
        for ingredient in [BurgerIngredients.BUNS[0], BurgerIngredients.FILLINGS[0]]:
            constructor_page.add_ingredient_to_order(ingredient)

        constructor_page.make_order()
        constructor_page.get_order_number()
        constructor_page.close_modal()

        # Переходим в ленту заказов
        constructor_page.click_feed_tab()
        feed_page.wait_for_orders_count_change(initial_total)

        # Проверяем счетчики
        assert feed_page.get_total_orders_count() > initial_total
        assert feed_page.get_today_orders_count() > initial_today

    @allure.story('Статусы')
    @allure.title('Проверка отображения заказа в работе')
    def test_order_in_progress(self, driver, login):
        feed_page = FeedPage(driver)
        constructor_page = ConstructorPage(driver)

        # Создаем заказ
        for ingredient in [BurgerIngredients.BUNS[0], BurgerIngredients.FILLINGS[0]]:
            constructor_page.add_ingredient_to_order(ingredient)

        constructor_page.make_order()
        order_number = constructor_page.get_order_number()
        constructor_page.close_modal()

        # Переходим в ленту заказов
        constructor_page.click_feed_tab()
        feed_page.wait_for_order_in_progress(order_number)

        # Проверяем отображение заказа
        assert feed_page.is_order_in_progress(order_number)