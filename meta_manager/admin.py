from django.contrib import admin
from .models import SEOSettings

# Register your models here.


@admin.register(SEOSettings)
class SEOSettingsAdmin(admin.ModelAdmin):
    list_display = ("page_name", "meta_title", "meta_description")
