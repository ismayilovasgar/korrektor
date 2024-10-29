from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "area_of_use",
        "phone_number",
        "is_active",
        "is_staff",
        "is_blocked",
        "daily_session",
        "location_city",
    )
