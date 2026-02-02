# Schools Project

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)

Простой Django-проект для работы с моделями школ и их директорами.  
Проект реализован в рамках учебного задания, с упором на **PEP8**, тестирование и работу с API.

---

## Реализованный функционал

- **REST API для школ**:
  - Создание, получение списка и деталей, обновление и удаление школ
- **Сериализация с вложенными данными директора**:
  - Автоматическое создание директора, если полного совпадения по `fio` и `birth_date` нет
- **Модульные тесты**:
  - Тесты сериализаторов и API с использованием `pytest`
- **Автоматизация качества кода**:
  - `ruff` для линтинга
  - `black` для автоформатирования (line-length = 79 для PEP8)
- Использование **PostgreSQL** через **Docker Compose**
- Конфигурация через `.env`

> На данный момент реализована только логика для школ.

---

## Технологии

- Python 3.12
- Django 6.0
- Django REST Framework
- PostgreSQL
- Docker Compose
- Pytest
- Ruff & Black

---

## Установка и настройка

1. **Клонируем репозиторий:**
```bash
git clone <repo_url>
cd <project_folder>
```

2. **Настройка виртуального окружения:**
```bash
python -m venv .venv
source .venv/bin/activate
```

3. **Установка зависимостей:**
```bash
pip install -r requirements.txt
```

4. **Настройка окружения:**
Создать .env файл в корне проекта
```env
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@db:5432/schools
```

5. **Запуск Docker Compose для бд:**
```bash
docker compose up
```

6. **Применение миграций:**
```bash
python manage.py migrate
```

7. **Запуск сервера:**
```bash
python manage.py runserver
```

## Тестирование

**Запуск тестов через pytest:**
```bash
pytest
```

**Проверка кода на соответствие pep8 через ruff:**
```bash
ruff check .
```

**Автоформатирование кода через black:**
```bash
black .
```