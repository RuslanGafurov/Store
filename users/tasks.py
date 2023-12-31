import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import EmailVerification, User


@shared_task
def send_email_verification(user_id) -> None:
    """Отложенная задача для отправки письма с кодом подтверждения электронной почты"""
    user = User.objects.get(id=user_id)
    record = EmailVerification.objects.create(
        user=user,
        code=uuid.uuid4(),
        expiration=now() + timedelta(hours=48),
    )
    record.send_verification_email()
