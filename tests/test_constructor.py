import pytest
import allure
from pages.constructor_page import ConstructorPage
from data import BurgerIngredients, Urls


@allure.feature('Конструктор бургеров')
class TestConstructor:
    @allure.story('Навигация')
    @allure.title('Переход в конструктор из ленты заказов')
    def test_navigate_to_constructor(self, driver):
        constructor_page = ConstructorPage(driver)
        constructor_page.open_page(Urls.FEED_URL)
        constructor_page.click_constructor_tab()
        current_url = constructor_page.get_current_url()
        assert current_url == Urls.CONSTRUCTOR_URL, \
            f"Ожидался URL {Urls.CONSTRUCTOR_URL}, получен {current_url}"

    @allure.story('Ингредиенты')
    @allure.title('Проверка модального окна ингредиента')
    @pytest.mark.parametrize('ingredient', BurgerIngredients.BUNS)
    def test_ingredient_details_modal(self, driver, ingredient):
        constructor_page = ConstructorPage(driver)
        constructor_page.scroll_to_buns_section()
        constructor_page.click_ingredient(ingredient)

        is_visible = constructor_page.is_ingredient_details_visible()
        assert is_visible, "Модальное окно с деталями ингредиента не отобразилось"

        constructor_page.close_modal()
        is_closed = not constructor_page.is_ingredient_details_visible()
        assert is_closed, "Модальное окно не закрылось"

    @allure.story('Ингредиенты')
    @allure.title('Проверка счетчика ингредиента')
    def test_ingredient_counter(self, driver, login):
        constructor_page = ConstructorPage(driver)
        ingredient = BurgerIngredients.BUNS[0]
        constructor_page.scroll_to_buns_section()

        initial_count = constructor_page.get_ingredient_counter(ingredient)
        constructor_page.add_ingredient_to_order(ingredient)
        new_count = constructor_page.get_ingredient_counter(ingredient)

        assert new_count == initial_count + 1, \
            f"Счетчик должен увеличиться с {initial_count} до {initial_count + 1}, получено {new_count}"

    @allure.story('Заказы')
    @allure.title('Проверка оформления заказа')
    def test_make_order(self, driver, login):
        constructor_page = ConstructorPage(driver)

        # Добавляем ингредиенты
        for ingredient in [BurgerIngredients.BUNS[0], BurgerIngredients.FILLINGS[0]]:
            section_name = 'Булки' if ingredient in BurgerIngredients.BUNS else 'Начинки'
            constructor_page.scroll_to_ingredient_section(section_name)
            constructor_page.add_ingredient_to_order(ingredient)

        constructor_page.make_order()
        order_number = constructor_page.get_order_number()

        assert order_number.isdigit(), \
            f"Номер заказа должен быть числом, получено '{order_number}'"
        assert len(order_number) > 0, \
            "Номер заказа не должен быть пустым"

        constructor_page.close_modal()
        is_closed = not constructor_page.is_ingredient_details_visible()
        assert is_closed, "Модальное окно заказа не закрылось"