from rest_framework import serializers
from django_app import models
from .models import User



class TextModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TextModel
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
        ]