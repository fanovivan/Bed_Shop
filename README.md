# Beds & Sofas — интернет-магазин мебели

Django-сайт для продажи кроватей и диванов с каталогом, фильтрами и корзиной.

## Возможности

- **Главная страница** — представление компании и популярные товары
- **Каталог** — список мебели с фильтрами по категории, цене, поиску и сортировке
- **Корзина** — добавление, изменение количества и удаление товаров (сессии)
- **Админ-панель** — управление категориями и товарами, загрузка изображений

## Быстрый старт

### 1. Активация виртуального окружения

```bash
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (cmd)
venv\Scripts\activate.bat

# Linux / macOS
source venv/bin/activate
```

### 2. Установка зависимостей (если venv ещё не настроен)

```bash
pip install -r requirements.txt
```

### 3. Миграции и тестовые данные

```bash
python manage.py migrate
python manage.py seed_data
```

### 4. Создание суперпользователя для админки

```bash
python manage.py createsuperuser
```

### 5. Запуск сервера

```bash
python manage.py runserver 8001
```

Сайт: http://127.0.0.1:8001/
Админка: http://127.0.0.1:8001/admin/

## Pre-commit

```bash
pre-commit install
pre-commit run --all-files
```

Хуки запускают: trailing-whitespace, end-of-file-fixer, black, isort, flake8.

## Структура проекта

```
bedssofas/
├── config/          # Настройки Django
├── shop/            # Приложение магазина
├── templates/       # HTML-шаблоны
├── static/          # CSS
├── media/           # Загруженные изображения (генерируется)
├── venv/            # Виртуальное окружение
└── manage.py
```

## Команды

| Команда | Описание |
|---------|----------|
| `python manage.py seed_data` | Заполнить БД примерами товаров |
| `python manage.py seed_data --clear` | Очистить и заново заполнить БД |
