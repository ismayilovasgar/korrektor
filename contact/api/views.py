from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactSerializer
from rest_framework.permissions import AllowAny
from django.conf import settings


def send_message(to_email, subject, message):
    """
    Ümumi bir mesaj göndərmə funksiyası.
    Həm istifadəçiyə, həm də sizin e-poçt ünvanınıza mesaj göndərə bilərsiniz.
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
        )
    except Exception as e:
        raise Exception(f"E-poçt göndərilərkən xəta baş verdi: {str(e)}")


@api_view(["POST"])
@permission_classes([AllowAny])
def create_contact(request):
    try:
        # ContactSerializer ilə verilənləri yoxlayırıq
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()

            try:
                # 1. İstifadəçinin mesajını sizin e-poçt ünvanınıza göndəririk
                send_message(
                    settings.DEFAULT_FROM_EMAIL,
                    f"Yeni Mesaj: {contact.full_name}",
                    f"Göndərən: {contact.full_name}\nMesaj: {contact.content}",
                )

                # 2. İstifadəçiyə məlumat mesajı göndəririk
                send_message(
                    contact.email,
                    f"Mesajınız Alındı: {contact.full_name}",
                    f"Salam {contact.full_name},\n\nMesajınız uğurla alındı.",
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
        # Serializer işləyərkən baş verən xətaları idarə edirik
        return Response(
            {"error": f"Xəta baş verdi: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
