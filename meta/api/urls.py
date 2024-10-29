from django.urls import path, include
from .views import *


urlpatterns = [
    path("seo/", list_seo_settings, name="list_seo_settings"),
    path("seo/page_name/<str:page_name>/", get_seo_settings, name="get_seo_settings"),
    path("seo/create/", create_seo_settings, name="create_seo_settings"),
    path("seo/update/<str:page_name>/", update_seo_settings, name="update_seo_settings"),
    path("seo/delete/<str:page_name>/", delete_seo_settings, name="delete_seo_settings"),
]
