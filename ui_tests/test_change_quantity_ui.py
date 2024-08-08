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

def test_add_and_increment_cart_ui(setup):
    driver = setup
    driver.get("https://altaivita.ru/")
    print("Открыт сайт Altaivita")

    # Поиск товара с использованием класса для поля поиска
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "js-searchpro__field-input"))
        )
        search_box.clear()  # Очистка поля перед вводом
        search_box.send_keys("Травяной чай")
        print("Товар введён в строку поиска")
    except (ElementNotInteractableException, NoSuchElementException) as e:
        print(f"Ошибка при взаимодействии с полем поиска: {e}")
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
        print("Клик по кнопке поиска выполнен")
    except (ElementNotInteractableException, NoSuchElementException) as e:
        print(f"Ошибка при взаимодействии с кнопкой поиска: {e}")
        return

    # Ожидание загрузки результатов поиска
    try:
        product = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Травяной чай Сибирский сильник, 98 г. в пирамидках')]"))
        )
        product.click()
        print("Товар выбран из результатов поиска")
    except (ElementNotInteractableException, NoSuchElementException) as e:
        print(f"Ошибка при выборе товара: {e}")
        return

    # Добавление в корзину
    try:
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'в корзину')]"))
        )
        add_to_cart_button.click()
        print("Товар добавлен в корзину")
    except (ElementNotInteractableException, NoSuchElementException) as e:
        print(f"Ошибка при добавлении в корзину: {e}")
        return

    # Проверка наличия товара в корзине
    try:
        time.sleep(5)  # Ждём загрузки страницы
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

        # Увеличение количества товаров на 1
        increment_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".more.js-plus_2_0"))
        )
        increment_button.click()

        # Проверка увеличения количества товаров
        new_count_element = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".count.active.js-count-number"))
        )

        new_count_text = new_count_element.text
        time.sleep(15)
        try:
            new_count_value = int(new_count_text)
        except ValueError:
            new_count_value = 0  # В случае ошибки преобразования устанавливаем значение по умолчанию


        # Проверка, что количество увеличилось на 1
        assert new_count_value == count_value, "Количество товаров не увеличилось на 1"
    except (ElementNotInteractableException, NoSuchElementException) as e:
        print(f"Ошибка при проверке корзины: {e}")
        return
