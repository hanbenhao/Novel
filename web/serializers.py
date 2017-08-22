from rest_framework import serializers
from web import models as web_models
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class userInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = web_models.userInfo
        fields = '__all__'