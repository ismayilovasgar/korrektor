from django.db import models
from django.contrib.auth.models import User
from helpers.models import TrackingModel
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
import pytz


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

    class Meta:
        ordering = ["-created_at"]  # Ən son düzəldilmiş mətni birinci göstər
        verbose_name = "Düzəldilmiş Mətn"
        verbose_name_plural = "Düzəldilmiş Mətinlər"

    def __str__(self):
        return f"Corrected by {self.user.username}: {self.text[:20]}"

    def clean(self):
        # Mətni müəyyən bir uzunluğa limitləmək
        if len(self.text) > 1000:  # Məsələn, maksimum 1000 simvol
            raise ValidationError("Mətn 1000 simvoldan uzun ola bilməz.")


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

    class Meta:
        ordering = ["-deleted_at"]  # Ən son silinmiş mətni birinci göstər
        verbose_name = "Silinmiş Mətn"
        verbose_name_plural = "Silinmiş Mətinlər"

    def __str__(self):
        return f"Deleted by {self.user.username}: {self.text[:20]}"

    def clean(self):
        # Mətni müəyyən bir uzunluğa limitləmək
        if len(self.text) > 1000:  # Məsələn, maksimum 1000 simvol
            raise ValidationError("Mətn 1000 simvoldan uzun ola bilməz.")
