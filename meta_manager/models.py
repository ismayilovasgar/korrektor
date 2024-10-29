from django.db import models

class SEOSettings(models.Model):
    page_name = models.CharField(max_length=25, unique=True)   # Hər səhifə üçün unikal ad
    meta_title = models.CharField(max_length=25)               # Meta başlıq
    meta_description = models.TextField(max_length=250)                       # Meta açıqlama

    def __str__(self):
        return self.page_name
