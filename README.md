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