from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


def send_password_reset_email(email):
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return  # Geçerli olmayan e-posta için işlem yapma

    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    reset_url = (
        # f"{settings.FRONTEND_URL}password-reset-confirm/?uidb64={uidb64}&token={token}/"
        f"{settings.FRONTEND_URL}password-reset-confirm/{uidb64}/{token}/"
    )

    send_mail(
        subject="Şifrəni sıfırla",
        message=f"Şifrənizi sıfırlamaq üçün bu linkə daxil olun: {reset_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )
