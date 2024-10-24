import os

import requests
from celery import Celery
from dotenv import load_dotenv

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Europe/Moscow',
    enable_utc=True,
)


@celery_app.task(name="send_notification_via_api")
def send_notification_via_api(chat_id: int, text: str) -> None:
    load_dotenv()
    api_token = os.environ.get("TOKEN")
    url = f"https://api.telegram.org/bot{api_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

