# Документация
Документация api:


```
http://localhost:8000/docs
```


# Запуск проекта

1. Клонируйте репозиторий:

```
git clone https://github.com/iMaanick/instant-messaging-service.git
```

2. При необходимости установить Poetry ```pip install poetry```

3. Запустить виртуальное окружение ```poetry shell```

4. Установить зависимости ```poetry install```


5. Добавьте файл .env и заполните его как в примере .example.env:

```
DATABASE_URI=postgresql+asyncpg://...
TOKEN=BOT_TOKEN
```
6. Выполнить для создания таблиц

```
alembic upgrade head 
```
7. Запустите redis

8. Для запуска выполните:
```
python -m app.main.bot
celery -A app.main.celery_app worker --loglevel=info --pool=solo
uvicorn --factory app.main:create_app --host localhost --port 8000
```

# Функциональность

1. Регистрация и аутентификация пользователей
2. Отправка и получение сообщений
3. Сохранение истории сообщений
4. Уведомления через Telegram-бота (никак не проверяется, заходил ли пользователь в бота до отправления уведомления. Поэтому пользователю необходимо предварительно зайти в бота и прописать команду /start )
5. Простенький интерфейс

# О проекте
1. FastAPI для разработки RESTful API
2. Fastapi-users для регистрации и аутентификации пользователей
3. PostgreSQL для хранения пользователей и сообщений
4. Redis для хранения сессий
5. SQLAlchemy для работы с базой данных
6. Alembic для управления миграциями
7. Celery отправки уведомлений через бота
8. WebSockets для реализации чата
9. Poetry для управления зависимостями


