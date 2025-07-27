from locators.constructor_locators import ConstructorLocators
from data import Urls, BurgerIngredients
import allure
from pages.base_page import BasePage

class ConstructorPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Кликнуть на вкладку 'Конструктор'")
    def click_constructor_tab(self):
        self.click_element_with_js(ConstructorLocators.CONSTRUCTOR_TAB)
        self.wait_for_url(Urls.CONSTRUCTOR_URL)

    @allure.step("Кликнуть на вкладку 'Лента заказов'")
    def click_feed_tab(self):
        self.click_element_with_js(ConstructorLocators.FEED_TAB)
        self.wait_for_url(Urls.FEED_URL)

    @allure.step("Добавить ингредиент в заказ")
    def add_ingredient_to_order(self, ingredient_name):
        section_name = 'Булки' if ingredient_name in BurgerIngredients.BUNS else 'Начинки'
        locator = f"//h2[text()='{section_name}']"
        self.scroll_to_element(locator)
        ingredient_locator = ConstructorLocators.INGREDIENT_ITEM.format(ingredient_name)
        self.drag_and_drop(ingredient_locator, ConstructorLocators.CONSTRUCTOR_AREA)

    @allure.step("Оформить заказ")
    def make_order(self):
        self.click_element(ConstructorLocators.ORDER_BUTTON)

    @allure.step("Получить номер заказа")
    def get_order_number(self):
        return self.get_element_text(ConstructorLocators.ORDER_MODAL)

    @allure.step("Закрыть модальное окно")
    def close_modal(self):
        self.click_element(ConstructorLocators.MODAL_CLOSE_BUTTON)
        self.wait_for_element_to_disappear(ConstructorLocators.INGREDIENT_DETAILS_MODAL)