# your_app/authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from core.exceptions import CustomTokenError  

class CustomJWTAuthentication(JWTAuthentication):

    def get_validated_token(self, raw_token):
        try:
            return super().get_validated_token(raw_token)
        except TokenError as e:
            # Burada özel hata mesajını oluşturuyoruz
            raise CustomTokenError(detail='Token etibarsızdır.', code='token_etibarsız')
