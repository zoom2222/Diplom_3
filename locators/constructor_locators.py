class ConstructorLocators:
    # Обновленные локаторы для хедера
    CONSTRUCTOR_TAB = "//a[contains(@href, '/') and .//p[contains(text(), 'Конструктор')]]"
    FEED_TAB = "//a[contains(@href, '/feed') and .//p[contains(text(), 'Лента заказов')]]"

    # Локаторы разделов
    BUNS_SECTION = "//h2[contains(text(), 'Булки')]/following-sibling::div[contains(@class, 'BurgerIngredients_ingredients')]"
    SAUCES_SECTION = "//h2[contains(text(), 'Соусы')]/following-sibling::div[contains(@class, 'BurgerIngredients_ingredients')]"
    FILLINGS_SECTION = "//h2[contains(text(), 'Начинки')]/following-sibling::div[contains(@class, 'BurgerIngredients_ingredients')]"

    # Локаторы ингредиентов
    INGREDIENT_ITEM = "//article[contains(@class, 'IngredientCard_card') and .//p[contains(text(), '{}')]]"
    INGREDIENT_COUNTER = "//p[contains(text(), '{}')]/ancestor::article//div[contains(@class, 'counter__num')]"

    # Модальное окно
    INGREDIENT_DETAILS_MODAL = "//div[contains(@class, 'Modal_modal')]//h2[contains(text(), 'Детали ингредиента')]"
    MODAL_CLOSE_BUTTON = "//button[contains(@class, 'Modal_close')]"

    # Кнопка заказа
    ORDER_BUTTON = "//button[contains(text(), 'Оформить заказ')]"
    ORDER_MODAL = "//div[contains(@class, 'Modal_modal')]//p[contains(@class, 'digits-large')]"