from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import SEOModel
from .serializers import SEOModelSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view


# GET: Bütün SEOModel obyektlərini əldə et
@api_view(["GET"])
def list_seo_settings(request):
    seo_settings = SEOModel.objects.all()  # Bütün qeydləri al
    serializer = SEOModelSerializer(seo_settings, many=True)  # Serializer ilə çevirmək
    return Response(serializer.data, status=status.HTTP_200_OK)


# GET: Səhifə adı ilə SEOModel məlumatını əldə et
@api_view(["GET"])
def get_seo_settings(request, page_name):
    try:
        seo_settings = SEOModel.objects.get(page_name=page_name)
        serializer = SEOModelSerializer(seo_settings)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except SEOModel.DoesNotExist:
        return Response(
            {"error": "SEO settings not found"}, status=status.HTTP_404_NOT_FOUND
        )


# POST: Yeni SEOModel obyekti yarat
@api_view(["POST"])
def create_seo_settings(request):
    serializer = SEOModelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PUT: SEOModel məlumatını tamamilə güncəllə
@api_view(["PUT"])
def update_seo_settings(request, page_name):
    try:
        seo_settings = SEOModel.objects.get(page_name=page_name)
        serializer = SEOModelSerializer(seo_settings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except SEOModel.DoesNotExist:
        return Response(
            {"error": "SEO settings not found"}, status=status.HTTP_404_NOT_FOUND
        )


# DELETE: SEOModel obyektini sil
@api_view(["DELETE"])
def delete_seo_settings(request, page_name):
    try:
        seo_settings = SEOModel.objects.get(page_name=page_name)
        seo_settings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except SEOModel.DoesNotExist:
        return Response(
            {"error": "SEO settings not found"}, status=status.HTTP_404_NOT_FOUND
        )
