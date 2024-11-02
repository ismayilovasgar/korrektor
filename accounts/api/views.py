from rest_framework.response import Response
from rest_framework import generics, status, response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone

# (
# LoginSerializer,
# UserSerializer,
# RegisterSerializer,
# CustomTokenObtainPairSerializer,
# CustomTokenRefreshSerializer,
# LogoutSerializer,
# TokenBlacklistSerializer,
# PasswordResetConfirmSerializer,
# PasswordResetSerializer,
# )
from rest_framework_simplejwt.exceptions import TokenError
from ..models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from ..utils.send_password_reset_email import *
from ..utils.send_verify_email import send_verification_email
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.encoding import force_str
import logging

# Logger yarat
logger = logging.getLogger(__name__)

User = get_user_model()


class VerifyEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, uidb64, token):
        try:
            User = get_user_model()
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            # Token təsdiqləmə nəzarəti
            try:
                AccessToken(token)
            except TokenError:
                return Response(
                    {"error": "geçersiz və ya süresi dolmuş token."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Email təsdiqləmə nəzarəti
            if user.is_email_verified:
                return Response(
                    {"error": "Email artıq doğrulanıb."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.is_active = True
            user.verify = True

            user.save()

            return Response(
                {"message": "Email təsdiq olundu!"}, status=status.HTTP_200_OK
            )
        #
        #
        except User.DoesNotExist:
            logger.error("UID ilə istifadəçi tapılmadı: %s", uid)
            return Response(
                {"error": "İstifadəçi tapılmadı."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.exception("Bir xəta baş verdi: %s", e)
            return Response(
                {"error": "Bir xəta baş verdi."}, status=status.HTTP_400_BAD_REQUEST
            )


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        try:
            return serializer.save()  # İstifadəçini yaradın
        except Exception as e:
            print(f"User creation error: {e}")  # Xətanı konsola yazdırın
            raise serializers.ValidationError({"detail": "İstifadəçi yaradılmadı."})

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # Xətaları avtomatik olaraq raise edir
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return response.Response(
                {"detail": "Validasiya xətası", "errors": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # İstifadəçini qeyd edin
        user = self.perform_create(serializer)

        if user is None:
            return response.Response(
                {"detail": "İstifadəçi yaradılmadı !"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # E-poçt doğrulama linkini göndərin
        send_verification_email(user)

        # Başlıq əlavə etmək istəsəniz
        headers = self.get_success_headers(serializer.data)

        return response.Response(
            {
                "detail": "Qeydiyyat uğurla başa çatdı, e-poçt doğrulama linki göndərildi!"
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Bloklanmış istifadəçini yoxlayın
            if user.is_blocked:
                return Response(
                    {"xəta": "Bu hesab bloklanıb"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # İstifadəçini avtomatik olaraq daxil olunmuş kimi qeyd edin
            login(request, user)

            # Mövcud tarixi yoxlayın və daily_session sahəsini yeniləyin
            today = timezone.now().date()
            if user.last_login and user.last_login.date() == today:
                user.daily_session += 1
            else:
                user.daily_session = 1
            user.save()

            # Yeni JWT token yarat
            refresh = RefreshToken.for_user(user)
            # user_data = UserSerializer(user).data

            # İstifadəçi məlumatlarını tokenə əlavə edin
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


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


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
