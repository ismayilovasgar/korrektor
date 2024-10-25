from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactSerializer
from rest_framework.permissions import AllowAny
from ..models import Contact


@api_view(["POST"])
def create_contact(request):
    permission_classes = [AllowAny,]
    serializer = ContactSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
