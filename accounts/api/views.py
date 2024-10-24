from rest_framework.response import Response
from rest_framework import generics, status, response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    LoginSerializer,
    UserSerializer,
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    LogoutSerializer,
    TokenBlacklistSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
)
from ..models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from ..utils.send_password_reset_email import send_password_reset_email
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # Hataları otomatik olarak raise eder (return gerekmez)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)  # Kullanıcıyı kaydet
        headers = self.get_success_headers(serializer.data)  # Başlık eklemek istersen

        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            # user_data = UserSerializer(user).data

            # Access token’ın içine kullanıcı bilgileri gömüyoruz
            refresh["username"] = user.username
            refresh["first_name"] = user.first_name
            refresh["last_name"] = user.last_name

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    # "user": user_data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"xəta": "Giriş məlumatları yanlışdır"}, status=status.HTTP_401_UNAUTHORIZED
        )


class ListUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# JWT token almak için görünüm
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# Token yenileme görünümü
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class LogoutView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"detail": "Uğurla çıxış edildi."}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenView(APIView):
    def post(self, request):
        serializer = TokenBlacklistSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"detail": "Token uğurla ləğv edildi."},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # E-posta göndərmə funksiyasını burada çağır
            send_password_reset_email(serializer.validated_data["email"])
            return Response(
                {"detail": "Şifrə sıfırlama e-poçtu göndərildi."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PasswordResetConfirmView(APIView):
class CustomPasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            # UID'yi çöz ve kullanıcıyı bul
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, OverflowError):
            raise ValidationError({"detail": "İstifadəçi tapılmadı."})

        # Token'in geçerli olup olmadığını kontrol et
        if not default_token_generator.check_token(user, token):
            raise ValidationError(
                {"detail": "Token keçərsizdir və ya vaxtı bitmişdir."}
            )

        # Şifre sıfırlama işlemi için serializer'ı kullan
        serializer = PasswordResetConfirmSerializer(
            data=request.data, context={"user": user}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"detail": "Şifrə uğurla yeniləndi."}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = "password_reset_confirm.html"
#     success_url = '/login/'
