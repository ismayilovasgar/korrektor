from django.contrib import admin
from .models import SEOModel

# Register your models here.


@admin.register(SEOModel)
class SEOSettingsAdmin(admin.ModelAdmin):
    list_display = ("page_name", "meta_title", "meta_description")
