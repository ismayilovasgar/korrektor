from rest_framework import serializers
from django.utils import timezone
from ..models import Contact
from validate_email_address import validate_email

class ContactSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ["full_name", "email", "content", "created_at", "updated_at"]

    def validate_full_name(self, value):
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("Ad Həriflərdən ibarət olmalıdır.")
        return value

    def validate_content(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Mesaj ən az 10 hərifdən ibarət olmalıdır.")
        return value

    def validate_email(self, value):
        # Düzgün Formatda email adresi
        if not validate_email(value):
            raise serializers.ValidationError("Düzgün bir email adresi girin.")
        return value

    def get_created_at(self, obj):
        # UTC zamanını yerli vaxta çeviririk
        return timezone.localtime(obj.created_at).strftime("%Y-%m-%d %H:%M:%S")

    def get_updated_at(self, obj):
        # UTC zamanını yerli vaxta çeviririk
        return timezone.localtime(obj.updated_at).strftime("%Y-%m-%d %H:%M:%S")
