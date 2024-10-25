from django.urls import path
from .views import create_contact

urlpatterns = [
    path("create/", create_contact, name="create-contact"),
]
