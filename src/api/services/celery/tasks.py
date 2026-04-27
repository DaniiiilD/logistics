import smtplib
from email.message import EmailMessage
from src.api.services.celery.celery_app import celery_instance
from src.core.config import settings
from src.core.constants import DEFAULT_EMAIL_FROM


@celery_instance.task
def send_notification_email(email: str, order_id: int, message: str):

    msg = EmailMessage()

    msg["Subject"] = f"Уведомление по заазу №{order_id}"
    msg["From"] = DEFAULT_EMAIL_FROM
    msg["To"] = email

    msg.set_content(message)

    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.send_message(msg)

        return f"Письмо успешно отправлено на {email}"

    except Exception as e:
        return f"Ошибка отправки: {str(e)}"
