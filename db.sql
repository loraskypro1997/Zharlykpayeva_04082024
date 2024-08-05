-- Вывести все уникальные названия продуктов
SELECT DISTINCT product_name
FROM Products;

-- Вывести id, название и стоимость продуктов с содержанием клетчатки (fiber) более 5 граммов
SELECT p.product_id, p.product_name, p.price
FROM Products p
JOIN Nutritional_Information n ON p.product_id = n.product_id
WHERE n.fiber > 5;

-- Вывести название продукта с самым высоким содержанием белка (protein)
SELECT p.product_name
FROM Products p
JOIN Nutritional_Information n ON p.product_id = n.product_id
ORDER BY n.protein DESC
LIMIT 1;

-- Подсчитать общую сумму калорий для продуктов каждой категории, исключая продукты с нулевым жиром (fat = 0)
SELECT c.category_id, SUM(p.calories) AS total_calories
FROM Products p
JOIN Categories c ON p.category_id = c.category_id
JOIN Nutritional_Information n ON p.product_id = n.product_id
WHERE n.fat > 0
GROUP BY c.category_id;

-- Рассчитать среднюю цену товаров каждой категории
SELECT c.category_name, AVG(p.price) AS average_price
FROM Products p
JOIN Categories c ON p.category_id = c.category_id
GROUP BY c.category_name;
