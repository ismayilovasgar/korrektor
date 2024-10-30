from rest_framework import serializers
from ..models import SEOModel


class SEOModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEOModel
        fields = ["page_name", "meta_title", "meta_description"]
        # read_only_fields = ['created_at', 'updated_at']

    def validate_page_name(self, value):
        if SEOModel.objects.filter(page_name=value).exists():
            raise serializers.ValidationError(
                {
                    "page_name": "Bu səyfə adı artıq mövcuddurr, xahiş edirəm başqa bir ad daxil edin."
                }
            )
        return value
