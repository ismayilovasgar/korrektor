from django.forms import ValidationError
from rest_framework import serializers
from ..models import User
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "CustomRegisterSerializer"
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "area_of_use",
        ]

        extra_kwargs = {
            "username": {
                "required": True,
                "error_messages": {
                    "required": _("İstifadəçi adı sahəsi boş qala bilməz."),
                },
            },
            "first_name": {
                "required": True,
                "error_messages": {
                    "required": _("İsim sahəsi boş qala bilməz."),
                },
            },
            "last_name": {
                "required": True,
                "error_messages": {
                    "required": _("Soyisim sahəsi boş qala bilməz."),
                },
            },
            "email": {
                "required": True,
                "error_messages": {
                    "required": _("E-posta sahəsi boş qala bilməz."),
                },
            },
            "password": {
                "required": True,
                "write_only": True,
                "error_messages": {
                    "required": _("Şifrə sahəsi boş qala bilməz."),
                },
            },
        }

    def create(self, validated_data):
        # print("Yaradılan məlumatlar:", validated_data)
        if User.objects.filter(username=validated_data["username"]).exists():
            raise serializers.ValidationError(
                {
                    "username": "Bu istifadəçi adı artıq alınmışdır, xahiş edirik başqa bir istifadəçi adı seçin."
                }
            )

        try:
            user = User(**validated_data)
            user.set_password(validated_data["password"])  # Şifrəni hash edin
            user.save()
            return user
        except Exception as e:
            raise serializers.ValidationError(
                {"error": "İstifadəçi yaradılarkən xəta baş verdi."}
            )

    def validate(self, data):
        try:
            validate_password(data["password"])  # Şifrəni yoxlayır
        except ValidationError as e:
            raise serializers.ValidationError({"password_errors": list(e.messages)})
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "area_of_use",
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Payload'a özel kul    lanıcı bilgilerini ekleyin
        token["username"] = user.username
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        # token["email"] = user.email
        # token["phone_number"] = user.phone_number
        # token["area_of_use"] = user.area_of_use

        return token


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Refresh token'ı çöz
        token = attrs["refresh"]
        decoded_data = self.get_token_payload(token)

        # Kullanıcıyı al
        user_model = get_user_model()
        user = user_model.objects.get(id=decoded_data["user_id"])

        # Yeni access token oluştur ve kullanıcı bilgilerini ekle
        data["access"] = self.get_access_token(user)

        return data

    def get_access_token(self, user):

        token = AccessToken.for_user(user)

        # Kullanıcı bilgilerini ekle
        token["username"] = user.username
        token["first_name"] = user.first_name
        # token["last_name"] = user.last_name

        return str(token)

    def get_token_payload(self, token):
        from rest_framework_simplejwt.tokens import UntypedToken

        # Token'ı çöz ve payload'ı al
        untyped_token = UntypedToken(token)
        return untyped_token.payload


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            # Refresh token-ı qara siyahıya əlavə et
            RefreshToken(self.token).blacklist()
        except Exception as e:
            raise serializers.ValidationError(
                "Etibarsız token və ya token artıq ləğv edilib."
            )


class TokenBlacklistSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            # Refresh token'ı blackliste ekle
            RefreshToken(self.token).blacklist()
        except Exception as e:
            raise serializers.ValidationError(
                "Token artıq etibarsızdır və ya öncə ləğv edilib."
            )


#
# password
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Bu e-poçt ünvanı ilə qeydiyyatdan keçən istifadəçi yoxdur."
            )
        return value


#
#


class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            uid = urlsafe_base64_decode(attrs["uidb64"]).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, OverflowError):
            raise serializers.ValidationError("İstifadəçi tapılmadı.")

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, attrs["token"]):
            raise serializers.ValidationError("Etibarsız və ya müddəti bitmiş token.")

        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()


#
#


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password1"] != attrs["new_password2"]:
            raise serializers.ValidationError({"detail": "Şifrələr uyğun deyil."})
        validate_password(attrs["new_password1"])
        return attrs

    def save(self, **kwargs):
        user = self.context["user"]
        user.set_password(self.validated_data["new_password1"])
        user.save()

