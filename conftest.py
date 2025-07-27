import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from data import Urls  # Убедитесь, что класс Urls существует в data.py

@pytest.fixture(params=['chrome', 'firefox'])
def driver(request):
    if request.param == 'chrome':
        options = ChromeOptions()
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
    elif request.param == 'firefox':
        options = FirefoxOptions()
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')
        driver = webdriver.Firefox(options=options)

    # Увеличиваем таймауты
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(10)

    try:
        driver.get(Urls.BASE_URL)
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script('return document.readyState') == 'complete')
    except Exception as e:
        pytest.fail(f"Не удалось загрузить страницу: {str(e)}")

    yield driver
    driver.quit()