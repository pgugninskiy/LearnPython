# 🛒 Домашнее задание: Class-Based Views и тестирование

## 🎯 Цель работы
Закрепить навыки работы с CBV (Class-Based Views) и написания автотестов с использованием Pytest.

## 🏆 Результат
Приложение интернет-магазина с функциональностью CRUD через CBV и тестами для ключевых функций.

---

## ✅ Выполненные требования

### 1. Реализация CBV для CRUD-операций
- [x] **ListView** — отображение списка товаров (`ProductListView`)
- [x] **DetailView** — отображение деталей товара (`ProductDetailView`)
- [x] **CreateView** — добавление нового товара (`ProductCreateView`)
- [x] **UpdateView** — редактирование товара (`ProductUpdateView`)
- [x] **DeleteView** — удаление товара с подтверждением (`ProductDeleteView`)

### 2. Тестирование с Pytest
- [x] **Тесты для модели (CRUD):**
  - `test_product_create` — создание товара
  - `test_product_read` — чтение товара из БД
  - `test_product_update` — обновление данных
  - `test_product_delete` — удаление товара
  - `test_product_str` — строковое представление
- [x] **Тесты для формы (валидация):**
  - `test_product_form_valid` — валидная форма
  - `test_product_form_invalid_price` — отрицательная цена
  - `test_product_form_missing_name` — отсутствие обязательного поля

---

## 📋 Соответствие критериям оценки
| Критерий оценки | Статус | Где реализовано |
| :--- | :---: | :--- |
| Реализованы CBV для CRUD-операций | ✅ | `shop/views.py` (5 классов) |
| Написаны тесты | ✅ | `shop/tests.py` (8 тестов) |

---

## 📁 Структура проекта
```text
Home_work_10/
├── manage.py
├── pytest.ini              # Настройки Pytest
├── config/                 # Настройки проекта
│   ├── settings.py
│   └── urls.py
└── shop/                   # Приложение магазина
    ├── models.py           # Модель Product
    ├── forms.py            # Формы с валидацией
    ├── views.py            # CBV (ListView, DetailView, CreateView, UpdateView, DeleteView)
    ├── urls.py             # Маршруты
    ├── admin.py            # Кастомизация админки
    ├── tests.py            # Pytest тесты (8 тестов)
    └── templates/shop/     # HTML-шаблоны
        ├── base.html
        ├── product_list.html
        ├── product_detail.html
        ├── product_form.html
        └── product_confirm_delete.html
```

---

## 🚀 Инструкция по запуску

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```
*Или установи вручную:*
```bash
pip install django pytest pytest-django
```

### 2. Применение миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Создание администратора
```bash
python manage.py createsuperuser
```

### 4. Запуск сервера
```bash
python manage.py runserver 8001
```

---

## 🧪 Запуск тестов

### Запустить все тесты:
```bash
pytest
```

### Запустить с подробным выводом:
```bash
pytest -v
```

### Запустить только тесты модели:
```bash
pytest shop/tests.py -k "test_product"
```

### Ожидаемый результат:
```
========= test session starts =========
collected 8 items

shop/tests.py::test_product_create PASSED
shop/tests.py::test_product_read PASSED
shop/tests.py::test_product_update PASSED
shop/tests.py::test_product_delete PASSED
shop/tests.py::test_product_str PASSED
shop/tests.py::test_product_form_valid PASSED
shop/tests.py::test_product_form_invalid_price PASSED
shop/tests.py::test_product_form_missing_name PASSED

========== 8 passed in 0.52s ==========
```

---

## 🔄 Сравнение FBV и CBV

| Операция | Function-Based View | Class-Based View |
| :--- | :--- | :--- |
| **Список товаров** | `def product_list(request): ...` | `class ProductListView(ListView): ...` |
| **Детали товара** | `def product_detail(request, pk): ...` | `class ProductDetailView(DetailView): ...` |
| **Создание** | `def product_create(request): ...` | `class ProductCreateView(CreateView): ...` |
| **Редактирование** | `def product_update(request, pk): ...` | `class ProductUpdateView(UpdateView): ...` |
| **Удаление** | ❌ Не было в предыдущем ДЗ | `class ProductDeleteView(DeleteView): ...` |

**Преимущества CBV:**
- ✅ Меньше кода (не нужно вручную обрабатывать GET/POST)
- ✅ Переиспользование логики через наследование
- ✅ Стандартизация (все разработчики пишут одинаково)
- ✅ Встроенная поддержка пагинации, форм, контекста

---

## 🧪 Сценарии для проверки

### 1. Проверка CBV:
- `http://127.0.0.1:8001/` — список товаров (ListView)
- `http://127.0.0.1:8001/product/1/` — детали товара (DetailView)
- `http://127.0.0.1:8001/product/new/` — создание (CreateView)
- `http://127.0.0.1:8001/product/1/edit/` — редактирование (UpdateView)
- `http://127.0.0.1:8001/product/1/delete/` — удаление (DeleteView)

### 2. Проверка тестов:
```bash
pytest -v
```
Все 8 тестов должны пройти успешно.

---

*Выполнил: Гугнинский П.*  
*Дата: Июнь 2026*