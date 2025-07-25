import pytest
import allure
import time
from selenium.webdriver.common.by import By
from pages.constructor_page import ConstructorPage
from data import BurgerIngredients, Urls


@allure.feature('Конструктор бургеров')
class TestConstructor:
    @allure.story('Навигация')
    @allure.title('Переход в конструктор из ленты заказов')
    def test_navigate_to_constructor(self, driver):
        constructor_page = ConstructorPage(driver)
        driver.get(Urls.FEED_URL)
        constructor_page.click_constructor_tab()
        assert driver.current_url == Urls.CONSTRUCTOR_URL

    @allure.story('Ингредиенты')
    @allure.title('Проверка модального окна ингредиента')
    @pytest.mark.parametrize('ingredient', BurgerIngredients.BUNS)
    def test_ingredient_details_modal(self, driver, ingredient):
        constructor_page = ConstructorPage(driver)
        buns_section = driver.find_element(By.XPATH, "//h2[text()='Булки']")
        driver.execute_script("arguments[0].scrollIntoView(true);", buns_section)
        time.sleep(1)  # Небольшая пауза для стабилизации

        constructor_page.click_ingredient(ingredient)
        assert constructor_page.is_ingredient_details_visible()
        constructor_page.close_modal()

    @allure.story('Ингредиенты')
    @allure.title('Проверка счетчика ингредиента')
    def test_ingredient_counter(self, driver, login):
        constructor_page = ConstructorPage(driver)
        ingredient = BurgerIngredients.BUNS[0]
        buns_section = driver.find_element(By.XPATH, "//h2[text()='Булки']")
        driver.execute_script("arguments[0].scrollIntoView(true);", buns_section)
        time.sleep(1)

        initial_count = constructor_page.get_ingredient_counter(ingredient)
        constructor_page.add_ingredient_to_order(ingredient)
        assert constructor_page.get_ingredient_counter(ingredient) == initial_count + 1

    @allure.story('Заказы')
    @allure.title('Проверка оформления заказа')
    def test_make_order(self, driver, login):
        constructor_page = ConstructorPage(driver)

        # Добавляем булку и начинку
        for ingredient in [BurgerIngredients.BUNS[0], BurgerIngredients.FILLINGS[0]]:
            section = driver.find_element(By.XPATH,
                                          f"//h2[text()='{'Булки' if ingredient in BurgerIngredients.BUNS else 'Начинки'}']")
            driver.execute_script("arguments[0].scrollIntoView(true);", section)
            time.sleep(1)
            constructor_page.add_ingredient_to_order(ingredient)

        constructor_page.make_order()
        order_number = constructor_page.get_order_number()
        assert order_number.isdigit()
        constructor_page.close_modal()