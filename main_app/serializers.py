from rest_framework import serializers
from .models import User, Course, Record
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
  confirm_password = serializers.CharField(write_only=True)

  class Meta: 
    model = User
    fields = ['email', 'username', 'password', 'confirm_password', 'role']
    extra_kwargs = {
      'password': {'write_only': True},
    }

  def validate(self, data): 
    if data['password'] != data['confirm_password']:
      raise serializers.ValidationError("Password and confirm password doesn't match")
    return data
  
  def create(self, validated_data):
    validated_data.pop('confirm_password')
    user = User.objects.create_user(
        email=validated_data['email'],
        username=validated_data['username'],
        role=validated_data['role'],
        password=validated_data['password']
    )
    return user
  
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class TokenPairSerializer(TokenObtainPairSerializer):
  username_field = User.EMAIL_FIELD

  @classmethod
  def get_token(self, user):
    token = super().get_token(user)
    token['email'] = user.email
    token['role'] = user.role
    return token
  
  def validate(self, params):
    data = super().validate(params)
    data['user'] = {
      'email': self.user.email,
      'username': self.user.username,
      'role': self.user.role,
    }
    return data
  
class CourseSerializer(serializers.ModelSerializer):
  class Meta:
    model = Course
    fields = '__all__'
    read_only_fields = ['id']

class RecordSerializer(serializers.ModelSerializer):
  class Meta:
    model = Record
    fields = '__all__'
    read_only_fields = ['id', 'created_at']