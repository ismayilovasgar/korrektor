from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import SEOModel
from .serializers import SEOModelSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def seo_model_list(request):
    if request.method == "GET":
        seo_models = SEOModel.objects.all()
        serializer = SEOModelSerializer(seo_models, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = SEOModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def seo_model_detail(request, page_name):
    try:
        seo_model = SEOModel.objects.get(page_name=page_name)
    except SEOModel.DoesNotExist:
        return Response(
            {"error": "Məlumat tapılmadı"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = SEOModelSerializer(seo_model)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = SEOModelSerializer(seo_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        serializer = SEOModelSerializer(seo_model, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        seo_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# # GET: Bütün SEOModel obyektlərini əldə et
# @api_view(["GET"])
# def list_seo_settings(request):
#     seo_settings = SEOModel.objects.all()  # Bütün qeydləri al
#     serializer = SEOModelSerializer(seo_settings, many=True)  # Serializer ilə çevirmək
#     return Response(serializer.data, status=status.HTTP_200_OK)


# # GET: Səhifə adı ilə SEOModel məlumatını əldə et
# @api_view(["GET"])
# def get_seo_settings(request, page_name):
#     try:
#         seo_settings = SEOModel.objects.get(page_name=page_name)
#         serializer = SEOModelSerializer(seo_settings)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except SEOModel.DoesNotExist:
#         return Response(
#             {"error": "SEO settings not found"}, status=status.HTTP_404_NOT_FOUND
#         )


# # POST: Yeni SEOModel obyekti yarat
# @api_view(["POST"])
# def create_seo_settings(request):
#     serializer = SEOModelSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # PUT: SEOModel məlumatını tamamilə güncəllə
# @api_view(["PUT"])
# def update_seo_settings(request, page_name):
#     try:
#         seo_settings = SEOModel.objects.get(page_name=page_name)
#         serializer = SEOModelSerializer(seo_settings, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     except SEOModel.DoesNotExist:
#         return Response(
#             {"error": "SEO settings not found"}, status=status.HTTP_404_NOT_FOUND
#         )


# # DELETE: SEOModel obyektini sil
# @api_view(["DELETE"])
# def delete_seo_settings(request, page_name):
#     try:
#         seo_settings = SEOModel.objects.get(page_name=page_name)
#         seo_settings.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     except SEOModel.DoesNotExist:
#         return Response(
#             {"error": "SEO settings not found"}, status=status.HTTP_404_NOT_FOUND
#         )
