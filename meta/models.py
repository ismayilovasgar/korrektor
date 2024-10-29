from django.db import models


# Create your models here.
class SEOModel(models.Model):

    page_name = models.CharField(
        max_length=25,
        unique=True,
        verbose_name="Səhifə adı",
    )
    meta_title = models.CharField(
        max_length=25,
        verbose_name="Meta başlıq",
    )
    meta_description = models.TextField(
        max_length=250,
        verbose_name="Meta açıqlama",
    )

    def __str__(self):
        return self.page_name
