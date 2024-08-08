import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

@pytest.fixture(scope="module")
def setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_add_to_cart_ui(setup):
    driver = setup
    driver.get("https://altaivita.ru/")

    # Поиск товара с использованием класса для поля поиска
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "js-searchpro__field-input"))
        )
        search_box.clear()  # Очистка поля перед вводом
        search_box.send_keys("Травяной чай")
    except (ElementNotInteractableException, NoSuchElementException) as e:
        print("Ошибка при взаимодействии с полем поиска:", e)
        return

    # Явное ожидание появления и доступности кнопки поиска
    try:
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".header__search .searchpro__field-button"))
        )

        # Прокрутка к элементу, если он перекрыт
        driver.execute_script("arguments[0].scrollIntoView(true);", search_button)

        # Попытка установления фокуса
        driver.execute_script("arguments[0].focus();", search_button)

        # Клик по кнопке поиска
        search_button.click()
    except (ElementNotInteractableException, NoSuchElementException) as e:
        print("Ошибка при взаимодействии с кнопкой поиска:", e)
        return

    # Ожидание загрузки результатов поиска
    try:
        product = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Травяной чай Сибирский сильник, 98 г. в пирамидках')]"))
        )
        product.click()
    except (ElementNotInteractableException, NoSuchElementException) as e:
        print("Ошибка при выборе товара:", e)
        return

    # Добавление в корзину
    try:
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'в корзину')]"))
        )
        add_to_cart_button.click()
    except (ElementNotInteractableException, NoSuchElementException) as e:
        print("Ошибка при добавлении в корзину:", e)
        return

    # Проверка наличия товара в корзине
    try:
        time.sleep(7)  # Ждём загрузки страницы
        cart_icon = driver.find_element(By.CLASS_NAME, "js-count-number")
        count_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".count.active.js-count-number"))
        )

        # Извлечение текста из элемента
        count_text = count_element.text

        # Преобразование текста в число
        try:
            count_value = int(count_text)
        except ValueError:
            count_value = 0  # В случае ошибки преобразования устанавливаем значение по умолчанию

        # Проверка значения
        if count_value == 0:
            print("Корзина пуста")
        else:
            print(f"В корзине {count_value} товаров")
        # Проверка с использованием assert для pytest
        assert count_value > 0, "Корзина пуста, ожидалось больше нуля"
    except (ElementNotInteractableException, NoSuchElementException) as e:
        print("Ошибка при проверке корзины:", e)
        return
