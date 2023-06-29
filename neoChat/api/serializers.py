from rest_framework import serializers,validators
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

#Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
  
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'password2')
        extra_kwargs = {
                    'username': {
                        'required': True, 
                        'allow_blank': False, 
                        'validators': [validators.UniqueValidator(User.objects.all(), "This username already exists")]
                        },
                    'first_name': {
                        'required': True
                        },
                    'last_name': {
                        'required': True
                        }
                    }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
                            username=validated_data['username'],
                            first_name=validated_data['first_name'],
                            last_name=validated_data['last_name']
                            )
        
        user.set_password(validated_data['password'])
        user.save()

        return user

