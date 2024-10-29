from rest_framework import serializers
from ..models import SEOModel


class SEOModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEOModel
        fields = ["page_name", "meta_title", "meta_description"]
        # read_only_fields = ['created_at', 'updated_at']
