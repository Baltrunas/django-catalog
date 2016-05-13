Api
===

Каталог категорий
---------------------

**/api/json/category/list/**

POST

    | username - логин для авторизации (requered)
    | password - пароль для авторизации (requered)

Варианты ответа:

Всё ок:

.. code-block:: javascript

    {
        "categories": [
            {
                "name": "Other",
                "parent": "None",
                "order": "None",
                "products_count": "12",
                "id": 1,
                "childs_count": "0",
                "slug": "other"
            },
        ]
    }

categories - сам список

Неправильный логин или пароль:

.. code-block:: javascript

    {"auth": false}


Добавление категории
---------------------

**/api/json/category/add/**

POST

    | username - логин для авторизации (requered)
    | password - пароль для авторизации (requered)
    | name - название категории (requered)
    | slug - ярлык категории (requered)
    | parent - родитель категории
    | order - порядок категории

Варианты ответа:

Всё ок:

.. code-block:: javascript

    {
        "status": true,
        "auth": true
    }

Если форма не валидна:

.. code-block:: javascript

        {
            "status": false,
            "auth": true
        }

Неправильный логин или пароль:

.. code-block:: javascript

        {"auth": false}


Редактирование категории
---------------------

**/api/json/category/update/$id/**

$id - id категории

POST

    | username - логин для авторизации (requered)
    | password - пароль для авторизации (requered)
    | name - название категории (requered)
    | slug - ярлык категории (requered)
    | parent - родитель категории
    | order - порядок категории

Варианты ответа:

Всё ок:

.. code-block:: javascript

    {
        "status": true,
        "auth": true
    }

Если форма не валидна:

.. code-block:: javascript

        {
            "status": false,
            "auth": true
        }

Неправильный логин или пароль:

.. code-block:: javascript

        {"auth": false}


Удаление категории
-------------------------

**/api/json/category/delete/$id/**

$id - id категории

POST

    |username - логин для авторизации
    |password - пароль для авторизации

Варианты ответа:

Всё ок:

.. code-block:: javascript

    {
        "status": true,
        "auth": true
    }

Неправильный логин или пароль:

.. code-block:: javascript

        {"auth": false}


Все продукты
-------------------------

**/api/json/product/list/**

POST

    |username - логин для авторизации
    |password - пароль для авторизации


Варианты ответа:

Всё ок:

.. code-block:: javascript

    {
        "products": [
            {
                "retail_price_with_discount": "350.0000",
                "description": "",
                "deleted": false,
                "wholesale_price": "350.0000",
                "barcode": "",
                "images": [
                    {
                        "image": "/media/catalog/1/None.jpg",
                        "id": 3,
                        "name": "тест",
                        "product_id": 1
                    }
                ],
                "retail_price": "350.0000",
                "id": 1,
                "category": "1",
                "name": "Сердце с крыльями",
                "cover": "/media/catalog/1/_cover.jpg",
                "main": true,
                "public": true
            },
        ],
        "auth": true
    }

"auth": true - говорит о том что аутентификация прошла успешно (иначе false и не будет списка)

products - сам список

Неправильный логин или пароль:

.. code-block:: javascript

        {"auth": false}


Создание товара
---------------------

**/api/json/product/add/**

POST

    |username - логин для авторизации
    |password - пароль для авторизации
    |name - name продукт
    |barcode - barcode продукт
    |category - category продукт
    |cover - cover продукт
    |description - description продукт
    |articul - articul продукт
    |retail_price - retail_price продукт
    |wholesale_price - wholesale_price продукт
    |retail_price_with_discount - retail_price_with_discount продукт
    |public - public продукт
    |main - main продукт

Варианты ответа:

Всё ок:

.. code-block:: javascript

    {
        "status": true,
        "auth": true
    }

Если форма не валидна:

.. code-block:: javascript

        {
            "status": false,
            "auth": true
        }

Неправильный логин или пароль:

.. code-block:: javascript

        {"auth": false}


Редактирование товара
---------------------

**/api/json/product/update/$id/**
$id - id продукта

POST

    |username - логин для авторизации
    |password - пароль для авторизации
    |name - name продукт
    |barcode - barcode продукт
    |category - category продукт
    |cover - cover продукт
    |description - description продукт
    |articul - articul продукт
    |retail_price - retail_price продукт
    |wholesale_price - wholesale_price продукт
    |retail_price_with_discount - retail_price_with_discount продукт
    |public - public продукт
    |main - main продукт

Варианты ответа:

Всё ок:

.. code-block:: javascript

    {
        "status": true,
        "auth": true
    }

Если форма не валидна:

.. code-block:: javascript

        {
            "status": false,
            "auth": true
        }

Неправильный логин или пароль:

.. code-block:: javascript

        {"auth": false}


Удаление продукта
-------------------------

**/api/json/product/delete/$id/**

$id - id продукта

POST

    |username - логин для авторизации
    |password - пароль для авторизации

Варианты ответа:

Всё ок:

.. code-block:: javascript

    {
        "status": true,
        "auth": true
    }

Неправильный логин или пароль:

.. code-block:: javascript

        {"auth": false}


Добавление изображения
-------------------------

**/api/json/image/add/$id/**

$id - id продукта

POST

    |username - логин для авторизации
    |password - пароль для авторизации
    |name - название изображения
    |image - изображение

Варианты ответа:

Всё ок:

.. code-block:: javascript

    {
        "status": true,
        "auth": true
    }

Если форма не валидна:

.. code-block:: javascript

        {
            "status": false,
            "auth": true
        }

Неправильный логин или пароль:

.. code-block:: javascript

        {"auth": false}


Удаление изображения
-------------------------

**/api/json/image/delete/$id/**

$id - id изображения

POST

    |username - логин для авторизации
    |password - пароль для авторизации

Варианты ответа:

Всё ок:

.. code-block:: javascript

    {
        "status": true,
        "auth": true
    }

Неправильный логин или пароль:

.. code-block:: javascript

        {"auth": false}