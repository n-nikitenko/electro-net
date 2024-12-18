# ElectroNet

**ElectroNet** — это веб-приложение на основе Django Rest Framework, предназначенное для управления иерархической сетью
по продаже электроники. Приложение позволяет создавать и поддерживать организованную структуру поставщиков и
дистрибьюторов, начиная с заводов и заканчивая индивидуальными предпринимателями, а также отслеживать задолженности и
управление продуктами.

## Основные возможности

- **Иерархическая структура:** Создание и управление сетью поставщиков с тремя уровнями:
    - Заводы (Уровень 0)
    - Розничные сети (Уровень 1)
    - Индивидуальные предприниматели (Уровень 2)

- **Управление отношениями с поставщиками:** Каждый узел сети ссылается на одного поставщика, а его уровень в иерархии
  определяется отношениями с другими узлами.

- **Управление продуктами:** Привязка продуктов к узлам сети, с указанием названия, модели и даты выхода на рынок.

- **Отслеживание задолженностей:** Учёт денежных задолженностей перед поставщиками с точностью до копейки.

- **Админ-панель Django:** Встроенный интерфейс для управления узлами сети и продуктами. Action для обнуления 
задолженности перед поставшиком у выбранных узлов сети.

- **REST API:** Возможность управления узлами и продуктами через API с поддержкой CRUD операций.

## Технологии

- [Django](https://www.djangoproject.com/) — фреймворк для быстрого веб-разработки.
- [Django REST Framework](https://www.django-rest-framework.org/) — инструмент для создания веб-API.
- [PostgreSQL](https://www.postgresql.org/) — рекомендуемая база данных для использования в продакшене.
- [DRF YASG](https://drf-yasg.readthedocs.io/en/stable/) - библиотека для генерации документации
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) - плагин Django Rest Framework для
  JWT-аутентификации
- [django-filter](https://django-filter.readthedocs.io/en/stable/) - приложение Django для фильтрации данных

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/n-nikitenko/ElectroNet.git
   cd ElectroNet
   ```
2. Заполните переменные окружения в файле .env
3. Запустите сервисы:
```commandline
    docker compose up --build -d
```
Приложение доступно по адресу: http://localhost:8080/

## Использование

### Админ-панель

- Доступ к панели администратора осуществляется по адресу http://localhost:8080/admin/ для управления узлами сети и продуктами.
- В админ-панели доступно действие Очистить задолженность перед поставщиком для обнуления долгов выбранных узлов.

2. Активируйте виртуальное окружение:
    ```
    poetry shell
    ```
3. Установите необходимые зависимости:
   ```poetry install```
4. Примените миграции для настройки базы данных:
   ```python manage.py migrate```
5. Создайте суперпользователя для доступа к админ-панели:
   ```python manage.py createsuperuser```
6. Запустите сервер разработки:
   ```python manage.py runserver```
7. Доступ к приложению:

- Документация: http://localhost:8080/
- Админ-панель: http://localhost:8080/admin/

### API

Приложение предоставляет следующие операции для управления узлами и продуктами:

- Получить список узлов сети.
- Создать новый узел сети.
- Получить информацию о конкретном узле сети.
- Обновить данные узла сети.
- Удалить узел сети.

Аналогичные операции можно выполнять с продуктами.

Список продуктов и узлов можно фильтровать по стране.

Реализована пагинация для списка объектов. Подробное описание api в документации.

### Модели

#### NetworkNode (Узел сети)

<table>
    <thead>
    <tr>
        <th>Поле</th>
        <th>Тип</th>
        <th>Описание</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td><code>name</code></td>
        <td><code>CharField</code></td>
        <td>Название узла сети (например, завод, розничная сеть).</td>
    </tr>
    <tr>
        <td><code>email</code></td>
        <td><code>EmailField</code></td>
        <td>Контактный email.</td>
    </tr>
    <tr>
        <td><code>country</code></td>
        <td><code>CharField</code></td>
        <td>Страна, где находится узел.</td>
    </tr>
    <tr>
        <td><code>city</code></td>
        <td><code>CharField</code></td>
        <td>Город, где находится узел.</td>
    </tr>
    <tr>
        <td><code>street</code></td>
        <td><code>CharField</code></td>
        <td>Улица, где находится узел.</td>
    </tr>
    <tr>
        <td><code>house_number</code></td>
        <td><code>CharField</code></td>
        <td>Номер дома, где находится узел.</td>
    </tr>
    <tr>
        <td><code>supplier</code></td>
        <td><code>ForeignKey</code></td>
        <td>Ссылка на поставщика (другой узел сети).</td>
    </tr>
    <tr>
        <td><code>debt_to_supplier</code></td>
        <td><code>IntegerField</code></td>
        <td>Задолженность перед поставщиком в копейках.</td>
    </tr>
    <tr>
        <td><code>created_at</code></td>
        <td><code>DateTimeField</code></td>
        <td>Дата и время создания узла сети (заполняется автоматически).</td>
    </tr>
    </tbody>
</table>

#### Product (Продукт)

<table>
    <thead>
    <tr>
        <th>Поле</th>
        <th>Тип</th>
        <th>Описание</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td><code>name</code></td>
        <td><code>CharField</code></td>
        <td>Название продукта.</td>
    </tr>
    <tr>
        <td><code>model</code></td>
        <td><code>CharField</code></td>
        <td>Модель продукта.</td>
    </tr>
    <tr>
        <td><code>release_date</code></td>
        <td><code>DateField</code></td>
        <td>Дата выхода продукта на рынок.</td>
    </tr>
    <tr>
        <td><code>network_node</code></td>
        <td><code>ForeignKey</code></td>
        <td>Узел сети, продающий этот продукт.</td>
    </tr>
    </tbody>
</table>

### Команды
- Заполнение тестовыми данными узлов сети:
    - При запуске команды можно указать количество заводов, розничных сетей и индивидуальных предпринимателей. Например:
        ```commandline
            poetry run python manage.py seed_network_nodes --factories=3 --retails=5 --individuals=10
        ```
- Заполнение тестовыми данными продуктов:
    - При запуске команды можно указать среднее количество продуктов, которое будет привязано к каждому узлу сети.. Например:
        ```commandline
            poetry run python manage.py seed_products --products-per-node=10        
        ```
- Проверка степени покрытия тестами (linux):
```commandline
        coverage run --source='.' manage.py test 
        coverage html  
```