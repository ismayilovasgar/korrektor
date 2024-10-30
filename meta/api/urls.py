from django.urls import path, include
from .views import *




urlpatterns = [
    path("seo/", seo_model_list, name="seo_model_list"),
    path("seo/<str:page_name>/", seo_model_detail, name="seo_model_detail"),
]
