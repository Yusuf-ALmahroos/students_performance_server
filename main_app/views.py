from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets

from .serializers import UserSerializer, TokenPairSerializer, CourseSerializer, RecordSerializer
from .models import Course, Record

class RegisterView(APIView):
  def post(self, request):
    serializer = UserSerializer(data = request.data)
    if(serializer.is_valid()): 
      user = serializer.save()
      return Response({'Message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
  serializer_class = TokenPairSerializer

class CourseViewSet(viewsets.ModelViewSet):
  queryset = Course.objects.all()
  serializer_class = CourseSerializer

class RecordViewSet(viewsets.ModelViewSet):
  queryset = Record.objects.all()
  serializer_class = RecordSerializer