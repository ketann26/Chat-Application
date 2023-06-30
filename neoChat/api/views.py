from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

import json

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.reverse import reverse
from rest_framework.parsers import JSONParser

from knox.auth import AuthToken

from .serializers import RegisterSerializer,OnlineUserSerializer,StartChatSerializer

@api_view(['POST'])
def login_api(request):

    serializer = AuthTokenSerializer(data = request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']

    _, token = AuthToken.objects.create(user)
    
    return Response({
        'user_info': {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            },
        'token': token,
    })

@api_view(['POST'])
def register_api(request):

    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    _, token = AuthToken.objects.create(user)

    return Response({
        'message': 'User created successfully'
    })

@api_view(['GET'])
def get_online_users_api(request):
    
    if request.method=='GET':

        users = get_user_model().objects.filter(email='1')
        serializer = OnlineUserSerializer(users,many=True)
    
    return Response(serializer.data)

@login_required
@api_view(['POST'])
def start_chat_api(request):
    
    if request.method=='POST':

        jsonData = JSONParser().parse(request)

        recipient_name = jsonData['username']
        recipient_obj = get_user_model().objects.filter(username=recipient_name)

        print(request.user.is_authenticated())

        if recipient_obj:
            recipient = recipient_obj[0]
            if recipient.email=='1':

                if request.user.id<recipient.id:
                    room_name = 'chat-{}-{}'.format(request.user.id,recipient.id)
                else:
                    room_name = 'chat-{}-{}'.format(recipient.idrequest.user.id,) 

                return Response({
                    'message': 'Success!',
                    'redirect_url': reverse('room',kwargs={'room_name':room_name})
                })
        
            return Response({
                'message': 'User is not available.'
            })
        
        return Response({
            'message': 'User does not exist'
        })


class SuggestFriends(APIView):

    def get(self, request, *args, **kwargs):     

        file_data = open('static/users.json')
        users = json.load(file_data)
        users_list = users['users']
        
        curr_user_id = self.kwargs["id"]
        for user in users_list:
            if user['id'] == curr_user_id:
                curr_user = user
                break

        user_interest_list = list(curr_user['interests'].keys())
        user_scores = {}
        for user in users_list:
            
            score = 0
            if abs(user['age']-curr_user['age']) < 5:

                for interest in user['interests']:
                    if interest in user_interest_list:
                        score = score + user['interests'][interest] + curr_user['interests'][interest]

                user_scores[user['id']] = score

        user_scores[curr_user_id] = 0

        sorted_user_scores = dict(sorted(user_scores.items(), key=lambda x:x[1],reverse=True))
        suggested_id_list = list(sorted_user_scores)[:5]

        suggested_friends = []
        for f_id in suggested_id_list:
            friend = next(item for item in users_list if item["id"] == f_id)
            suggested_friends.append(friend)

        return Response({"suggested_friends": suggested_friends})


    

    