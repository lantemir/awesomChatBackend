from rest_framework import serializers
from django_app import models
from .models import User



class TextModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TextModel
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'username',
            'name',

        ]
    
    def get_name(self, obj):
        fname = obj.first_name.capitalize()
        lname = obj.last_name.capitalize()
        return fname + ' ' + lname
    
class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password'
        ]
        extra_kwargs ={
            'password': {
                #Гарантирует, что при сериализации это поле будет исключено
                'write_only': True
            }
        }
    def create(self, validated_data):
        username = validated_data['username'].lower()
        first_name = validated_data['first_name'].lower()
        last_name = validated_data['last_name'].lower()

        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        password = validated_data['password']
        user.set_password(password)
        user.save()
        return user
