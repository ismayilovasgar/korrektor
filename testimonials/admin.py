from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'profession', 'feedback', 'user', 'slug')  # Görünəcək sahələr
    search_fields = ('full_name', 'profession', 'feedback')  # Axtarışda istifadə ediləcək sahələr
    list_filter = ('profession',)  # Filtrləmə üçün istifadə ediləcək sahələr

    # Əlavə parametrləri burada konfiqurasiya edə bilərsiniz
