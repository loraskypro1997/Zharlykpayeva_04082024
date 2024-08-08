
# Altaivita Cart Tests

## Описание

Этот проект содержит тесты для функционала корзины интернет-магазина Altaivita. Тесты охватывают как API, так и UI функционал.

## Установка

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Запустите тесты:
   ```bash
   pytest --alluredir=allure-results
   ```

3. Откройте отчёт Allure:
   ```bash
   allure serve allure-results
   ```

## Структура проекта

- `api_tests/`: Тесты для API
- `ui_tests/`: Тесты для UI
- `requirements.txt`: Зависимости проекта

## Тесты

### API

1. **Add to Cart**: Проверка добавления товара в корзину через API.
2. **Delete from Cart**: Проверка удаления товара из корзины через API.

### UI

1. **Add to Cart UI**: Проверка добавления товара в корзину через интерфейс.
2. **Change Quantity UI**: Проверка изменения количества товара через интерфейс.
