from django.contrib import admin
from .models import Contact


# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        # "__str__",
        "title",
        "content",
        "first_name",
        "last_name",
        # "created_at",
        "updated_at",
    )
