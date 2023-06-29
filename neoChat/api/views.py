from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken

from .serializers import RegisterSerializer

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

# class UserDetailAPI(APIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (AllowAny,)
#     def get(self,request,*args,**kwargs):
#         user = User.objects.get(id=request.user.id)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)

# #Class based view to register user
# class RegisterUserAPIView(generics.CreateAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = RegisterSerializer
