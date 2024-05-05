from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import base64
from django.core.files.base import ContentFile
from django_app import models
from .serializers import SignUpSerializer, ProfileSerializer, UserSerializer

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        user = self.scope['user']
        print (user, user.is_authenticated)
        if not user.is_authenticated:
            return
        #safe username to use as a group name for this user
        self.username = user.username

        #join this user to a group with their username
        async_to_sync(self.channel_layer.group_add)(
            self.username, self.channel_name
        )

        self.accept()
    
    def disconnect(self, close_code):
        #leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.username, self.channel_name
        )


    #handle request
    def receive(self, text_data):
        data = json.loads(text_data)
        data_source = data.get('source')

        print('receive', json.dumps(data, indent=2))

        # Thumbnail upload
        if data_source == 'thumbnail':
            self.receive_thumbnail(data)
        
    def receive_thumbnail(self, data):
        user = self.scope['user']
        print('user@@@', user)
        profile = user.profile
        #convert base64 data to django content file
        image_str = data.get('base64')
        image = ContentFile(base64.b64decode(image_str))
        #upload thubnail field
        filename = data.get('filename')
        profile.avatar.save(filename, image, save=True)
        #serialize user
        #serialized = ProfileSerializer(profile)


        prof = models.Profile.objects.get(user = user)
        serialized ={
        'user': UserSerializer(user).data,        
        'profile': ProfileSerializer(prof).data
        
        }
        print("receive_thumbnail_serialized@@@", serialized)


        #send updated user data including new thumbnail
        print("self.username@@@", self.username)
       
        self.send_group(self.username, 'thumbnail', serialized)


        # Catch/ all broadcast to client helper

    def send_group(self, group, source, data):
        response = {
                'type': 'broadcast_group',
                'source':source,
                'data': data
        }     
        async_to_sync(self.channel_layer.group_send)(
            group, response
        )
    
    def broadcast_group(self, data):
        '''
        data: 
            - type: 'broadcast_group'
            - source: where it originated from
            - data: what ever you want to send as a dict
        '''
        data.pop('type')
         
            # data:             
            #     - source: where it originated from
            #     - data: what ever you want to send as a dict
        
        self.send(text_data=json.dumps(data))
