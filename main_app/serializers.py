from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
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