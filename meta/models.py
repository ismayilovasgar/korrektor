from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator


# Create your models here.
class SEOModel(models.Model):

    page_name = models.CharField(
        max_length=20,
        unique=True,
        error_messages={
            "unique": _(
                "Bu səhifə adı artıq mövcuddur, xahiş edirəm başqa bir ad daxil edin."
            ),
        },
    )

    meta_title = models.CharField(
        max_length=30,
        validators=[
            MaxLengthValidator(
                30, message=_("Meta başlıq 25 simvoldan uzun ola bilməz.")
            )
        ],
    )

    meta_description = models.TextField(
        max_length=250,
        validators=[
            MaxLengthValidator(
                250, message=_("Meta açıqlama 250 simvoldan uzun ola bilməz.")
            )
        ],
    )

    def __str__(self):
        return self.page_name
