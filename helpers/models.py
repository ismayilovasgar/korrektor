from django.db import models
from django.utils import timezone


# Create your models here.
class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def formatted_created_at(self):
        return timezone.localtime(self.created_at).strftime("%d-%m-%Y %H:%M:%S")

    def formatted_updated_at(self):
        return timezone.localtime(self.updated_at).strftime("%d-%m-%Y %H:%M:%S")

    class Meta:
        abstract = True
        ordering = ("-created_at",)
