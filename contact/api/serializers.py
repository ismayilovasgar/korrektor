from rest_framework import serializers
from django.utils import timezone
from ..models import Contact


class ContactSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ["full_name", "email", "content", "created_at", "updated_at"]

    def get_created_at(self, obj):
        # UTC zamanını yerli vaxta çeviririk
        return timezone.localtime(obj.created_at).strftime("%Y-%m-%d %H:%M:%S")

    def get_updated_at(self, obj):
        # UTC zamanını yerli vaxta çeviririk
        return timezone.localtime(obj.updated_at).strftime("%Y-%m-%d %H:%M:%S")
