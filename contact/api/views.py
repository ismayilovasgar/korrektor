from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactSerializer
from rest_framework.permissions import AllowAny
from django.conf import settings


@api_view(["POST"])
def create_contact(request):
    permission_classes = [
        AllowAny,
    ]

    # ContactSerializer ilə verilənləri yoxlayırıq
    try:
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            # Verini qeyd et
            contact = serializer.save()

            try:
                # E-poçt göndərmə əməliyyatı - İstifadəçinin e-poçt ünvanına
                send_mail(
                    # E-poçtun mövzusu
                    subject=f"Mesajınız Alındı: {contact.full_name}",
                    # Mesajın məzmunu
                    message=f"Salam {contact.full_name},\n\nMesajınız uğurla alındı. Məzmunu:\n\n{contact.content}",
                    # Göndərən e-poçt ünvanı, settings.py-dən götürülür
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    # İstifadəçinin e-poçt ünvanına göndəriləcək
                    recipient_list=[contact.email],
                )

                return Response(
                    {"message": "Mesaj uğurla göndərildi.", "contact": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                # E-poçt göndərmə xətası
                return Response(
                    {"error": f"E-poçt göndərilərkən xəta baş verdi: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(
            {"error": "Göndərilən məlumatlar düzgün deyil."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    except Exception as e:
        # Serializatoru işləyərkən baş verən xətaları idarə edir
        return Response(
            {"error": f"Xəta baş verdi: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
