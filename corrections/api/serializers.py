from rest_framework import serializers
from ..models import CorrectedText, DeletedText


class CorrectedTextSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = CorrectedText
        fields = ["username", "text", "created_at", "updated_at"]
        read_only_fields = ["user", "created_at", "updated_at"]


class DeletedTextSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = DeletedText
        fields = ["username", "text", "deleted_at"]
        read_only_fields = ["user", "deleted_at"]
