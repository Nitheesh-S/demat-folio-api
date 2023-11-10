import time
from django.core.mail import send_mail

from . import models, utils


def create_user(name: str, email: str, password: str):
    user = models.User(
        username=email, email=email, first_name=name, is_active=False
    )
    user.set_password(password)
    user.save()
    message = f"{time.time()}::{user.pk}"
    token = utils.encrypt_message(message)

    send_mail(
        subject="DematFolio email verification",
        message=f"Hi verify email with this path /verify-email?token={token}",
        from_email="nitheeshmsk@gmail.com",
        recipient_list=[email],
        fail_silently=False,
    )
    
    return user


def activate_user(user_id: int):
    models.User.objects.filter(pk=user_id).update(is_active=True)