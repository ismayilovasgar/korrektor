from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import SEOSettings
from .serializers import SEOSettingsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import api_view


@api_view(["POST"])
def create_seo_setting(request):
    serializer = SEOSettingsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_seo_setting(request, page_name):
    try:
        seo_setting = SEOSettings.objects.get(page_name=page_name)
    except SEOSettings.DoesNotExist:
        return Response(
            {"detail": "SEO setting not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = SEOSettingsSerializer(seo_setting)
    return Response(serializer.data)


@api_view(["PUT", "PATCH"])
def update_seo_setting(request, page_name):
    try:
        seo_setting = SEOSettings.objects.get(page_name=page_name)
    except SEOSettings.DoesNotExist:
        return Response(
            {"detail": "SEO setting not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = SEOSettingsSerializer(seo_setting, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_seo_setting(request, page_name):
    try:
        seo_setting = SEOSettings.objects.get(page_name=page_name)
    except SEOSettings.DoesNotExist:
        return Response(
            {"detail": "SEO setting not found."}, status=status.HTTP_404_NOT_FOUND
        )

    seo_setting.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# !apiview
# # Bütün obyektləri göstərmək və yeni obyekt yaratmaq
# class SEOSettingsListView(generics.ListCreateAPIView):
#     queryset = SEOSettings.objects.all()
#     serializer_class = SEOSettingsSerializer
#     permission_classes = [IsAuthenticated]


# # Spesifik bir obyekti göstərmək
# class SEOSettingsRetrieveView(generics.RetrieveAPIView):
#     queryset = SEOSettings.objects.all()
#     serializer_class = SEOSettingsSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         page_name = self.kwargs.get("page_name")
#         return generics.get_object_or_404(SEOSettings, page_name=page_name)


# # Spesifik bir obyekti yeniləmək
# class SEOSettingsUpdateView(generics.UpdateAPIView):
#     queryset = SEOSettings.objects.all()
#     serializer_class = SEOSettingsSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         page_name = self.kwargs.get("page_name")
#         return generics.get_object_or_404(SEOSettings, page_name=page_name)


# # Spesifik bir obyekti silmək
# class SEOSettingsDestroyView(generics.DestroyAPIView):
#     queryset = SEOSettings.objects.all()
#     serializer_class = SEOSettingsSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         page_name = self.kwargs.get("page_name")
#         return generics.get_object_or_404(SEOSettings, page_name=page_name)


# ! viewset
# class SEOSettingsViewSet(viewsets.ModelViewSet):

#     queryset = SEOSettings.objects.all()
#     serializer_class = SEOSettingsSerializer
#     permission_classes = [IsAuthenticated]

## Bütün obyektləri göstərmək üçün list metodu
# def list(self, request, *args, **kwargs):
#     queryset = self.get_queryset()
#     serializer = self.get_serializer(queryset, many=True)
#     return Response(serializer.data)

# ## GET metodu - müəyyən page_name-ə görə obyekti tapır
# def retrieve_by_page_name(self, request, page_name=None):
#     try:
#         seo_setting = self.queryset.get(page_name=page_name)
#         serializer = self.get_serializer(seo_setting)
#         return Response(serializer.data)
#     except SEOSettings.DoesNotExist:
#         return Response(
#             {"detail": "SEO setting tapılmadı."}, status=status.HTTP_404_NOT_FOUND
#         )

# ## PUT metodu - müəyyən page_name-ə görə obyekti tam yeniləyir
# def update_by_page_name(self, request, page_name=None):
#     try:
#         seo_setting = self.queryset.get(page_name=page_name)
#         serializer = self.get_serializer(seo_setting, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     except SEOSettings.DoesNotExist:
#         return Response(
#             {"detail": "SEO setting tapılmadı."}, status=status.HTTP_404_NOT_FOUND
#         )

# ## PATCH metodu - müəyyən page_name-ə görə obyekti qismən yeniləyir
# def partial_update_by_page_name(self, request, page_name=None):
#     try:
#         seo_setting = self.queryset.get(page_name=page_name)
#         serializer = self.get_serializer(
#             seo_setting, data=request.data, partial=True
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     except SEOSettings.DoesNotExist:
#         return Response(
#             {"detail": "SEO setting tapılmadı."}, status=status.HTTP_404_NOT_FOUND
#         )

# ## DELETE metodu - müəyyən page_name-ə görə obyekti silir
# def delete_by_page_name(self, request, page_name=None):
#     try:
#         seo_setting = self.queryset.get(page_name=page_name)
#         seo_setting.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     except SEOSettings.DoesNotExist:
#         return Response(
#             {"detail": "SEO setting tapılmadı."}, status=status.HTTP_404_NOT_FOUND
#         )
