from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Testimonial
from .serializers import TestimonialSerializer


@api_view(["GET", "POST"])
# İstifadəçinin autentikasiya olunmasını tələb edir
@permission_classes([IsAuthenticated])
def testimonial_list_create(request):
    if request.method == "GET":
        try:
            testimonials = Testimonial.objects.all()
            serializer = TestimonialSerializer(testimonials, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    elif request.method == "POST":
        serializer = TestimonialSerializer(data=request.data)
        if serializer.is_valid():
            # İstifadəçi məlumatlarını əlavə et
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
# İstifadəçinin autentikasiya olunmasını tələb edir
def testimonial_detail(request, slug):
    try:
        # Slug-a əsaslanan tapma
        testimonial = Testimonial.objects.get(slug=slug)
    except Testimonial.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TestimonialSerializer(testimonial)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TestimonialSerializer(testimonial, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        serializer = TestimonialSerializer(testimonial, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        testimonial.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
