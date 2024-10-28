from django.db import models
from django.contrib.auth.models import User
from helpers.models import TrackingModel
from django.conf import settings


class CorrectedText(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="corrected_texts",
        null=True,
        blank=True,
    )
    text = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Corrected by {self.user.username}: {self.text[:20]}"


class DeletedText(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="deleted_texts",
        null=True,
        blank=True,
    )
    text = models.TextField(max_length=255)
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deleted by {self.user.username}: {self.text[:20]}"
