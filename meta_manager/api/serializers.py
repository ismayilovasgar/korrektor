from rest_framework import serializers
from ..models import SEOSettings


class SEOSettingsSerializer(serializers.ModelSerializer):
    page_name = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "required": "Səyfə adı daxil edilməlidir.",
            "blank": "Səyfə adı boş ola bilməz.",
        },
    )
    meta_title = serializers.CharField()
    meta_description = serializers.CharField()

    class Meta:
        model = SEOSettings
        fields = "__all__"

    def validate_page_name(self, value):
        if SEOSettings.objects.filter(page_name=value).exists():
            raise serializers.ValidationError(
                {
                    "page_name": "Bu səyfə adı artıq mövcuddur, xahiş edirəm başqa bir ad daxil edin."
                }
            )
        return value
