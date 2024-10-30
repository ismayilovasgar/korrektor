from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
import re

class Testimonial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="testimonials")
    full_name = models.CharField(max_length=50)
    profession = models.CharField(max_length=50)
    feedback = models.TextField(max_length=500, verbose_name="Rəyin mətni", unique=True)
    profile_picture = models.ImageField(upload_to="testimonials/", null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def clean(self):
        if self.feedback == "":
            raise ValidationError("Rəy boş ola bilməz")
        if len(self.feedback) < 10:  # Minimum 10 simvol tələb olunur
            raise ValidationError("Rəy ən azı 10 simvol uzunluğunda olmalıdır.")
        
        # Şəkil validasiyası
        if self.profile_picture:
            width, height = get_image_dimensions(self.profile_picture)
            if width > 800 or height > 800:  # Maksimum ölçü 800x800 piksel
                raise ValidationError("Profil şəkli 800x800 piksel ölçüsündən kiçik olmalıdır.")
            if not self.profile_picture.name.endswith(('.png', '.jpg', '.jpeg')):  # Yalnız PNG, JPG, JPEG formatlarına icazə verilir
                raise ValidationError("Profil şəkli yalnız PNG, JPG və JPEG formatlarında olmalıdır.")

    def save(self, *args, **kwargs):
        if not self.slug and self.feedback:
            # Feedback dəyərini kiçik hərflərlə slug-a çevirir
            feedback_normalized = self.feedback.strip().lower()  
            feedback_normalized = re.sub(r'[^a-z0-9\s-]', '', feedback_normalized)
            feedback_normalized = re.sub(r'[\s]+', '-', feedback_normalized)

            self.slug = slugify(feedback_normalized)  

            # Unikal slug yaratmaq
            counter = 1
            while Testimonial.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{counter}"
                counter += 1
        else:
            # Feedback dəyişdikdə slug-ı yenilə
            if self.slug and self.feedback:
                feedback_normalized = self.feedback.strip().lower()  
                feedback_normalized = re.sub(r'[^a-z0-9\s-]', '', feedback_normalized)
                feedback_normalized = re.sub(r'[\s]+', '-', feedback_normalized)
                new_slug = slugify(feedback_normalized)
                if new_slug != self.slug:
                    self.slug = new_slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/testimonials/{self.slug}/"

    def __str__(self):
        return f"{self.full_name} - {self.profession}"


# from django.db import models
# from django.conf import settings
# from django.utils.text import slugify
# from django.core.exceptions import ValidationError
# import re 

# # Create your models here.

# class Testimonial(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="testimonials")
#     full_name = models.CharField(max_length=50)

#     profession = models.CharField(max_length=50)

#     feedback = models.TextField(max_length=500, verbose_name="Rəyin mətni", unique=True,)
#     profile_picture = models.ImageField(upload_to="testimonials/", null=True, blank=True)

#     slug = models.SlugField(max_length=200, unique=True, blank=True)


#     def clean(self):
#         if self.feedback == "":
#             raise ValidationError("Rəy boş ola bilməz")

#     def save(self, *args, **kwargs):
#         if not self.slug and self.feedback:
#             # Feedback dəyərini kiçik hərflərlə slug-a çevirir
#             feedback_normalized = self.feedback.strip().lower()  # Boşluqları sil və kiçik hərflərə çevir
            
#             # Xüsusi simvolları silmək
#             feedback_normalized = re.sub(r'[^a-z0-9\s-]', '', feedback_normalized)
            
#             # Boşluqları defislə əvəz etmək
#             feedback_normalized = re.sub(r'[\s]+', '-', feedback_normalized)

#             self.slug = slugify(feedback_normalized)  # slugify funksiyası boşluqları defis ilə əvəz edir
            
#             # Unikal slug yaratmaq
#             counter = 1
#             while Testimonial.objects.filter(slug=self.slug).exists():
#                 self.slug = f"{self.slug}-{counter}"
#                 counter += 1
            
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.full_name} - {self.profession}"
