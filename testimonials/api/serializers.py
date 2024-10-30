from django.conf import settings
from rest_framework import serializers
from ..models import Testimonial
from django.contrib.auth import get_user_model

# User = settings.AUTH_USER_MODEL
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class TestimonialSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Testimonial
        fields = "__all__"
