from django.urls import path
from . import views

urlpatterns = [

    # Rəyləri siyahı və yarat
    path('feedbacks/', views.testimonial_list_create, name='testimonial-list-create'),  

    # Rəyə əsaslanan təfsilatı
    path('feedbacks/<slug:slug>/', views.testimonial_detail, name='testimonial-detail'),  

]
