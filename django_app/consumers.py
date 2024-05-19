from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import base64
from django.core.files.base import ContentFile
from django_app import models
from .serializers import SignUpSerializer, ProfileSerializer, UserSerializer, SearchSerializer, RequestSerializer, SearchSerializerTest

from django.db.models import Q, Exists, OuterRef
from .models import User, Connection

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        user = self.scope['user']
        print ("user.is_authenticated@@@", user.is_authenticated)
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
        try:  
            data = json.loads(text_data)
            data_source = data.get('source')

            print("receive_data_source!!!@@@ " , data_source)

             
            # Make friend request
            if data_source == 'request.accept':
                self.receive_request_accept(data)

            
            # Make friend request
            elif data_source == 'request.connect':
                self.receive_request_connect(data)

            # GET equest.list
            elif data_source == 'request.list':
                self.receive_request_list(data)
            
            # Search / filter users
            elif data_source == 'search':
                self.receive_search(data)

            # Thumbnail upload
            elif data_source == 'thumbnail':
                self.receive_thumbnail(data)
            else:
                print("Unknown message type:")
                # message_type = data['type']
                
        except ValueError as e:
            print("Error processing message:", str(e))
           


    def receive_request_accept(self, data):
        username = data.get('username')
        #fetch connection objects
        try:
            connection =Connection.objects.get(
                sender__username=username,
                receiver = self.scope['user']
            )
        except Connection.DoesNotExist:
            print('Error: connection doesnt exists')
            return
        connection.accepted = True
        connection.save()

        serialized = RequestSerializer(connection)
        # Send accepted request to sender
        self.send_group(
            connection.sender.username, 'request.accept', serialized.data
        )
        # Send accepted request to receiver
        self.send_group(
            connection.receiver.username, 'request.accept', serialized.data
        )

    def receive_request_list(self, data):

        user = self.scope['user']

        # Get connection  made to this user
        connections = Connection.objects.filter(
            receiver=user,
            accepted=False
        )
       
        serialized = RequestSerializer(connections, many=True)
        # Send request lit back to this user
        self.send_group(user.username, 'request.list', serialized.data)

    def receive_request_connect(self, data):
        username = data.get('username')
        try:
            receiver = User.objects.get(username=username)
        except User.DoesNotExist:
            print('Error user not found')
            return
        ##Create connection##
        connection, _ = Connection.objects.get_or_create(
            sender=self.scope['user'],
            receiver=receiver
        )
        ##serialized connection##
   
        serialized = RequestSerializer(connection)

        # Send back to sender##
        self.send_group(connection.sender.username, 'request.connect', serialized.data)

        ##Send to receiver##
        self.send_group(
            connection.receiver.username, 'request.connect', serialized.data
        )



    def receive_search(self, data):
        
        query = data.get('query')       
        
       
        # print("test_users.query@@@: ", test_users.query) // можно проверить sql
 

        users = User.objects.filter(
            Q(username__istartswith=query) |
            Q(first_name__istartswith=query) |
            Q(last_name__istartswith=query)
        ).exclude(            
            username=self.username
        ).annotate(
            pending_them=Exists(
                Connection.objects.filter(
                    sender = self.scope['user'],
                    receiver=OuterRef('id'),
                    accepted=False
                )
            ),
            pending_me=Exists(
                Connection.objects.filter(
                    sender = OuterRef('id'),
                    receiver=self.scope['user'],
                    accepted=False
                )
            ),
            connected=Exists(
                Connection.objects.filter(
                  Q(sender=self.scope['user'], receiver=OuterRef('id') ) |
                  Q(receiver=self.scope['user'], sender=OuterRef('id') ),
                  accepted=True
            ),   
            )       
        )

        print("receive_search_receive_search@", users)
        # serialize results
        serialized = SearchSerializer(users, many=True)

        print("receive_search_data@@@", serialized.data)
  
        # Send search results back to this user
        self.send_group(self.username, 'search', serialized.data)
        
    def receive_thumbnail(self, data):
        user = self.scope['user']

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
    


        #send updated user data including new thumbnail
  
       
        self.send_group(self.username, 'thumbnail', serialized)


        # Catch/ all broadcast to client helper

    def send_group(self, group, source, data):

        print("source!!!", source)
        print("data!!!", data)
        print("group!!!", group)
        print("self!!!", self)
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
        print("data___broadcast_group", data)
      
        # data.pop('type')
         
            # data:             
            #     - source: where it originated from
            #     - data: what ever you want to send as a dict
     
        
        self.send(text_data=json.dumps(data))
