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
