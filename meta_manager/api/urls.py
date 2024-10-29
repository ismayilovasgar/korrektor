from django.urls import path, include

# from rest_framework.routers import DefaultRouter
# from .views import SEOSettingsViewSet
# from .views import SEOSettingsAPIView

# router = DefaultRouter()
# router.register(r'seo-settings', SEOSettingsViewSet, basename='seo-settings')

# urlpatterns = [
#     # path("", include(router.urls)),

#     ## page-name ilə bir obyekti göstərmək üçün URL
#     path('seo-settings/page-name/<str:page_name>/', SEOSettingsViewSet.as_view({
#         'get': 'retrieve_by_page_name',
#         'put': 'update_by_page_name',
#         'patch': 'partial_update_by_page_name',
#         'delete': 'delete_by_page_name'
#     }), name='seo-settings-by-page-name'),
# ]

# from .views import (
#     seo_settings_list,
#     seo_setting_detail,
#     update_seo_setting,
#     partial_update_seo_setting,
#     delete_seo_setting,
# )


# --------------------------------------------------
# from .views import (
#     SEOSettingsListView,
#     SEOSettingsRetrieveView,
#     SEOSettingsUpdateView,
#     SEOSettingsDestroyView,
# )

# urlpatterns = [
#     # Bütün obyektləri göstərmək və yeni obyekt yaratmaq
#     path("seo-settings/", SEOSettingsListView.as_view(), name="seo-settings-list-create"),

#     # Spesifik obyekti göstərmək
#     path("seo-settings/page-name/<str:page_name>/",SEOSettingsRetrieveView.as_view(),name="seo-settings-retrieve",),

#     # Spesifik obyekti yeniləmək
#     path("seo-settings/page-name/<str:page_name>/update/",SEOSettingsUpdateView.as_view(),name="seo-settings-update",),

#     # Spesifik obyekti silmək
#     path("seo-settings/page-name/<str:page_name>/delete/",SEOSettingsDestroyView.as_view(),name="seo-settings-destroy"),
# ]

from .views import *




urlpatterns = [
    path('seo-settings/', create_seo_setting, name='create_seo_setting'),
    path('seo-settings/<str:page_name>/', get_seo_setting, name='get_seo_setting'),
    path('seo-settings/<str:page_name>/update/', update_seo_setting, name='update_seo_setting'),
    path('seo-settings/<str:page_name>/delete/', delete_seo_setting, name='delete_seo_setting'),
]
