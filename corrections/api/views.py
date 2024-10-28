import jwt
from django.conf import settings
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from ..models import CorrectedText, DeletedText
from rest_framework.permissions import IsAuthenticated
from .serializers import CorrectedTextSerializer, DeletedTextSerializer
from rest_framework.decorators import api_view, permission_classes


# class LastThreeCorrectedTextsView(generics.ListAPIView):
#     serializer_class = CorrectedTextSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return CorrectedText.objects.filter(user=self.request.user).order_by(
#             "-corrected_at"
#         )[:3]


# class LastThreeDeletedTextsView(generics.ListAPIView):
#     serializer_class = DeletedTextSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return DeletedText.objects.filter(user=self.request.user).order_by(
#             "-deleted_at"
#         )[:3]


# class LastCorrectedTextsView(APIView):
#     def get(self, request):
#         # Son 3 doğrulanmış metni al
#         corrected_texts = CorrectedText.objects.order_by("-created_at")[:3]
#         serializer = CorrectedTextSerializer(corrected_texts, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class LastDeletedTextsView(APIView):
#     def get(self, request):
#         # Son 3 silinmiş metni al
#         deleted_texts = DeletedText.objects.order_by("-deleted_at")[:3]
#         serializer = DeletedTextSerializer(deleted_texts, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_last_corrected_texts(request):
    # Son 3 duzeltilmis metni al
    corrected_texts = CorrectedText.objects.order_by("-created_at")[:3]
    serializer = CorrectedTextSerializer(corrected_texts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_last_deleted_texts(request):
    # Son 3 silinmiş metni al
    deleted_texts = DeletedText.objects.order_by("-deleted_at")[:3]
    serializer = DeletedTextSerializer(deleted_texts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_corrected_text(request):
    token = request.headers.get("Authorization", "").split(" ")[1]

    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username = decoded_data.get("username")
        User = get_user_model()  # Özelleştirilmiş istifadəçi modelini al
        user = User.objects.get(username=username)

        text = request.data.get("text")
        if not text:
            return Response(
                {"error": "Metin alanı boş olamaz"}, status=status.HTTP_400_BAD_REQUEST
            )

        corrected_text = CorrectedText.objects.create(text=text, user=user)
        serializer = CorrectedTextSerializer(corrected_text)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except jwt.ExpiredSignatureError:
        return Response(
            {"error": "Token süresi dolmuş"}, status=status.HTTP_401_UNAUTHORIZED
        )
    except jwt.InvalidTokenError:
        return Response(
            {"error": "Geçersiz token"}, status=status.HTTP_401_UNAUTHORIZED
        )
    except User.DoesNotExist:
        return Response(
            {"error": "Kullanıcı bulunamadı"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_deleted_text(request):
    token = request.headers.get("Authorization", "").split(" ")[1]

    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username = decoded_data.get("username")
        User = get_user_model()  # Özelleştirilmiş istifadəçi modelini al
        user = User.objects.get(username=username)

        text = request.data.get("text")
        if not text:
            return Response(
                {"error": "Metin alanı boş olamaz"}, status=status.HTTP_400_BAD_REQUEST
            )

        deleted_text = DeletedText.objects.create(text=text, user=user)
        serializer = DeletedTextSerializer(deleted_text)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except jwt.ExpiredSignatureError:
        return Response(
            {"error": "Token süresi dolmuş"}, status=status.HTTP_401_UNAUTHORIZED
        )
    except jwt.InvalidTokenError:
        return Response(
            {"error": "Geçersiz token"}, status=status.HTTP_401_UNAUTHORIZED
        )
    except User.DoesNotExist:
        return Response(
            {"error": "Kullanıcı bulunamadı"}, status=status.HTTP_404_NOT_FOUND
        )
