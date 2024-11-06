from django.db import models
from helpers.models import TrackingModel
from datetime import datetime


# Create your models here.
class Contact(TrackingModel):
    full_name = models.CharField(max_length=40)
    email = models.EmailField(max_length=60)
    content = models.TextField(max_length=200)

    def __str__(self):
        return f"{self.full_name} | {self.email}"

    # def save(self, *args, **kwargs):
    #     now = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    #     if not self.created_at:
    #         self.created_at = now   # İlk yaradıldığında created_at qeyd edilir
    #     self.updated_at = now       # Hər yeniləmə zamanı updated_at yenilənir
    #     super().save(*args, **kwargs)
