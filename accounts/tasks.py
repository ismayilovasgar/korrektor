# your_app/tasks.py

from celery import shared_task
from django.utils import timezone
from .models import User


@shared_task
def reset_daily_sessions():
    # Burada gündəlik sessiyaları sıfırlamaq üçün kod yazın
    # Məsələn:
    User.objects.all().update(daily_session=0)
    print(f"Gündəlik sessiyalar sıfırlandı: {timezone.now()}")
