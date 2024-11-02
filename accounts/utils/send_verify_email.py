from rest_framework import status
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import secrets


def generate_verification_code(length=6):
    # 6 simvoldan ibarət təsadüfi kod yaradır
    return secrets.token_hex(length)


def send_verification_email(user):
    try:
        # JWT token yaradın
        token = AccessToken.for_user(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Təsadüfi doğrulama kodunu yaradın
        verification_code = generate_verification_code(length=6)

        # İstifadəçinin modelindəki verification_code sahəsini güncəlləyin
        user.verification_code = verification_code
        user.save()

        link = reverse("verify-email", kwargs={"uidb64": uid, "token": str(token)})
        verification_link = (
            f"{settings.VERIFICATION_BASE_URL}{link}?code={verification_code}"
        )

        try:
            send_mail(
                subject="Email Təsdiqləmək !",
                message=f"Zəhmət olmazsa hesabiniz təsdiq etmək üçün bu linkə keçin: {verification_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

        except Exception as e:
            print(f"E-poçt göndərilərkən xəta: {e}")

    except ObjectDoesNotExist:
        print("İstifadəçi tapılmadı.")
    except Exception as e:
        print(f"Xəta baş verdi: {e}")
