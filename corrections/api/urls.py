from django.urls import path
from .views import (
    # LastThreeCorrectedTextsView,
    # LastThreeDeletedTextsView,
    save_corrected_text,
    save_deleted_text,
    get_last_corrected_texts,
    get_last_deleted_texts
)

urlpatterns = [
    # path("last-three-corrected/",LastThreeCorrectedTextsView.as_view(),name="last-three-corrected"),
    # path("last-three-deleted/",LastThreeDeletedTextsView.as_view(),name="last-three-deleted"),

    path("last-corrected-texts/", get_last_corrected_texts, name="last_corrected_texts"),
    path("last-deleted-texts/", get_last_deleted_texts, name="last_deleted_texts"),
    path("save-corrected-text/", save_corrected_text, name="save_corrected_text"),
    path("save-deleted-text/", save_deleted_text, name="save_deleted_text"),
]
