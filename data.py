class Credentials:
    email = 'oleg_shatohin_22_333@ya.ru'  # Замените на реальные данные
    password = 'olegoleg'        # Замените на реальные данные

class BurgerIngredients:
    BUNS = ['Флюоресцентная булка R2-D3', 'Краторная булка N-200i']
    SAUCES = ['Соус Spicy-X', 'Соус фирменный Space Sauce']
    FILLINGS = ['Мясо бессмертных моллюсков Protostomia', 'Биокотлета из марсианской Магнолии']

class Urls:
    BASE_URL = 'https://stellarburgers.nomoreparties.site'
    LOGIN_URL = f'{BASE_URL}/login'
    REGISTER_URL = f'{BASE_URL}/register'
    PROFILE_URL = f'{BASE_URL}/account/profile'
    FEED_URL = f'{BASE_URL}/feed'
    CONSTRUCTOR_URL = f'{BASE_URL}/'