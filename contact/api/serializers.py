from rest_framework import serializers
from ..models import Contact


class ContactSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = [
            "first_name",
            "last_name",
            "email",
            "title",
            "content",
            "created_at",
            "updated_at",
        ]

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d,%H:%M:%S")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%Y-%m-%d, %H:%M:%S")

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)

    ##    <== Customize the representation if needed ==>
    #     return {
    #         "Contact Information": {
    #             "ID": representation["id"],
    #             "Name": representation["name"],
    #             "Surname": representation["surname"],
    #             "Email": representation["email"],
    #             "Title": representation["title"],
    #             "Content": representation["content"],
    #             "Created At": representation["created_at"],
    #         }
    #     }
