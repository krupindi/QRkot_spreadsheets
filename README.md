# Проект QRkot_spreadseets
![python version](https://img.shields.io/badge/Python-3.9-green)

## О проекте

QRkot - это благотворительный фонд поддержки котиков. Наша цель - сбор пожертвований для различных целевых проектов, таких как медицинское обслуживание, обустройство кошачьих колоний и обеспечение кормом. Мы стремимся помочь нуждающимся кошкам получить всё необходимое для комфортной жизни.

## Ключевые функции

- Управление проектами: Возможность создавать, редактировать и удалять целевые проекты;
- Система пожертвований: Пожертвования распределяются по принципу First In, First Out, обеспечивая приоритетность ранним проектам;
- Прозрачность и доступность: Все пользователи могут просматривать списки проектов и пожертвований;
- Авторизация и аутентификация: Защита данных пользователей и проектов с использованием JWT.

## Дополнительные функции

- Генерация отчётов в Google Sheets: Автоматическое создание отчётов по закрытым проектам с сортировкой по скорости сбора средств.

## Установка и запуск

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/krupindi/QRkot_spreadsheets.git
```

```
cd QRkot_spreadsheets
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать и заполнить .env файл по шаблону .env_template

```
APP_TITLE=...
APP_DESCRIPTION=...
DATABASE_URL=sqlite+aiosqlite:///./YOUR_DB_NAME.db
SECRET=YOUR_SECRET_KEY
FIRST_SUPERUSER_EMAIL=...
FIRST_SUPERUSER_PASSWORD=...
TYPE=...
PROJECT_ID=...
PRIVATE_KEY_ID=...
PRIVATE_KEY="..."
CLIENT_EMAIL=...
CLIENT_ID=...
AUTH_URI=...
TOKEN_URI=...
AUTH_PROVIDER_X509_CERT_URL=...
CLIENT_X509_CERT_URL=...
EMAIL=...
```

Выполнить миграции:

```
alembic upgrade head
```

Запустить приложение:

```
uvicorn app.main:app --reload
```

- Swagger - http://127.0.0.1:8000/docs
- Redoc - http://127.0.0.1:8000/redoc

## Работа с Google Sheets

Для работы с Google Sheets, вам понадобятся учетные данные сервисного аккаунта Google. Вот как их получить:

- [Переходите в консоль облачной платформы](https://console.cloud.google.com) и авторизуйтесь(для того чтобы работать с Google Cloud Platform, нужен гугл-аккаунт);
- Создайте новый проект;
- Перейдите в раздел "APIs & Services" -> "Credentials";
- Нажмите "Create credentials" и выберите "Service account";
- Заполните необходимые поля и создайте учетную запись;
- На странице учетной записи создайте ключ в формате JSON;
- Скачайте файл с ключом и скопируйте его содержимое .env файл;
- После этого вы сможете сгенерировать отчет через Swagger эндпоинт '/google'
- Отчет будет сохранен на вашем Google Диске

## Автор проекта

Крупин Дмитрий
