import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from ..models import CorrectedText, DeletedText
from rest_framework.permissions import IsAuthenticated
from .serializers import CorrectedTextSerializer, DeletedTextSerializer
from rest_framework.decorators import api_view, permission_classes


#! <== get user from sended token==>
def get_user_from_token(request):
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None, Response(
            {"error": "token tapılmadı"}, status=status.HTTP_401_UNAUTHORIZED
        )

    token = auth_header.split(" ")[1]

    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username = decoded_data.get("username")
        User = get_user_model()
        user = User.objects.get(username=username)
        return user, None

    except jwt.ExpiredSignatureError:
        return None, Response(
            {"error": "token müddəti bitmiş"}, status=status.HTTP_401_UNAUTHORIZED
        )
    except jwt.InvalidTokenError:
        return None, Response(
            {"error": "keçərsiz token"}, status=status.HTTP_401_UNAUTHORIZED
        )
    except User.DoesNotExist:
        return None, Response(
            {"error": "istifadəçi tapılmadı"}, status=status.HTTP_404_NOT_FOUND
        )


#! <==== ----------------------------------------------------------------------------- ===>


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_last_corrected_texts(request):
    ## token-dan istifadəçi məlumatını al
    user, error_response = get_user_from_token(request)
    if error_response:
        return error_response

    ## <== istifadəçiyə aid son 3 düzəldilmiş mətni al ==>
    corrected_texts = CorrectedText.objects.filter(user=user)[:3]
    serializer = CorrectedTextSerializer(corrected_texts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_last_deleted_texts(request):
    ## token-dan istifadəçi məlumatını al
    user, error_response = get_user_from_token(request)
    if error_response:
        return error_response

    ## <== istifadəçiyə aid son 3 silinmiş mətni al ==>
    deleted_texts = DeletedText.objects.filter(user=user)[:3]
    serializer = DeletedTextSerializer(deleted_texts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_corrected_text(request):
    ## token-dan istifadəçi məlumatını al
    user, error_response = get_user_from_token(request)
    if error_response:
        return error_response

    text = request.data.get("text")
    if not text:
        return Response(
            {"error": "mətin sahəsi boş ola bilməz"}, status=status.HTTP_400_BAD_REQUEST
        )

    ## Düzəldilmiş mətni saxla
    corrected_text = CorrectedText.objects.create(text=text, user=user)
    serializer = CorrectedTextSerializer(corrected_text)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_deleted_text(request):
    user, error_response = get_user_from_token(request)
    if error_response:
        return error_response

    text = request.data.get("text")
    if not text:
        return Response(
            {"error": "mətin sahəsi boş ola bilməz"}, status=status.HTTP_400_BAD_REQUEST
        )

    ## Silinmiş mətni saxla
    deleted_text = DeletedText.objects.create(text=text, user=user)
    serializer = DeletedTextSerializer(deleted_text)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
