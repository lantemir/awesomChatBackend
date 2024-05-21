from rest_framework import serializers
from django_app import models
from .models import User, Connection, Message



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
    
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    avatar = serializers.ImageField()

    class Meta:
        model = models.Profile
        fields = [
            'user',
            'avatar',
            
        ]

        
    
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


class SearchSerializer(UserSerializer):
    status = serializers.SerializerMethodField()
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = [
            'username',
            'name',
            #'thumbnail',
            'status',
            'profile'
        ]
    def get_status(self, obj):
        if obj.pending_them:
            return 'pending-them'
        elif obj.pending_me:
            return 'pending-me'
        elif obj.connected:
            return 'connected'
        return 'no-connection'
    
# class AddProfileSerializer(UserSerializer):   
#     profile = ProfileSerializer()

#     class Meta:
#         model = User
#         fields = [                    
#             'profile'
#         ]
class AddProfileSerializer(serializers.ModelSerializer):    
    name = serializers.SerializerMethodField()
    avatar = serializers.ImageField(source='profile.avatar')

    class Meta:
        model = User
        fields = [
            'username',
            'name',
            'avatar'
        ]
    
    def get_name(self, obj):
        fname = obj.first_name.capitalize()
        lname = obj.last_name.capitalize()
        return f"{fname} {lname}"
    
    
    
class RequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()
    senderprofile = ProfileSerializer(source='sender.profile')    
    user = serializers.SerializerMethodField()

    class Meta: 
        model = Connection
        fields = [
                'id',
                'sender',
                'receiver',
                'created',
                'senderprofile',
                'user'              
        ]
    def get_user(self, obj):
        receiver = obj.receiver
        user_data = {
            'username': receiver.username,
            'name': f"{receiver.first_name} {receiver.last_name}"
            # Здесь вы можете добавить другие поля пользователя, если необходимо
        }
        return user_data
    
class FriendSerializer(serializers.ModelSerializer):
    friend =serializers.SerializerMethodField()
    preview = serializers.SerializerMethodField()

    class Meta:
        model = Connection
        fields = [
            'id',
            'friend',
            'preview',
            'updated'          
        ]
    
    def get_friend(self, obj):
        # If I am a sender
        if self.context['user'] == obj.sender:
            return AddProfileSerializer(obj.receiver).data
        # If I am  receiver
        elif self.context['user'] == obj.receiver:
            return AddProfileSerializer(obj.sender).data
        else:
            print('Error: No user found in friendSerializer')
        
    def get_preview(self, data):
        return 'New connection'
    

class MessageSerializer(serializers.ModelSerializer):
    is_me = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()

    class Meta:
        model=Message
        fields = [
            'id',
            'is_me',
            'text',
            'created',
            'profile'

        ]

    def get_is_me(self, obj):
        return self.context['user'] == obj.user
    
    def get_profile(self, obj):
        return AddProfileSerializer(obj.user).data
