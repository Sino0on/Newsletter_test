from newsletter.celery import app
from django.core.mail import send_mail
from .models import Message
import requests
import datetime
from datetime import datetime, timezone


@app.task
def start_newsletter(payload, end_date):
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTkzMzA5MjAsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9TaW5vMG9uIn0.TBpfsuntfLE48Xf9320uyQ-vCAIEOOU2lW8TxcXt82A",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "Accept": "*/*"
    }
    url = f'https://probe.fbrq.cloud/v1/send/{payload["id"]}'
    current_datetime = datetime.now(timezone.utc)
    end_datetime = datetime.fromisoformat(end_date)
    if current_datetime < end_datetime:
        data = requests.post(url, json=payload, headers=headers)
        print(data.status_code)
        if data.status_code == 200:
            message = Message.objects.get(id=payload['id'])
            message.status = 'OK'
            message.save()



