import smtplib
from email.message import EmailMessage
from src.api.services.celery.celery_app import celery_instance
from core.config import settings
from src.core.constants import DEFAULT_EMAIL_FROM


@celery_instance.task
def send_email_to_driver(driver_email: str, order_id: int):

    msg = EmailMessage()

    msg["Subject"] = f"Новый заказ №{order_id} для вас!"
    msg["From"] = DEFAULT_EMAIL_FROM
    msg["To"] = driver_email

    msg.set_content(
        "Здравствуйте! Для вашей машины появилась новая заявка на перевозку. Пожалуйста, зайдите в приложение"
    )

    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.send_message(msg)

        return f"Письмо успешно отправлено на {driver_email}"

    except Exception as e:
        return f"Ошибка отправки: {str(e)}"
