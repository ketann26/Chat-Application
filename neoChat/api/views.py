from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
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


    

    