from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializers(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

        extra_kwargs = {
            'password' : {
                'write_only' : True
            }
        }

    def create(self, validated_data):

        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')

        # Confirm passwords are the same
        if password != password2:
            raise serializers.ValidationError({
                "error": "Passwords must be the same"
            })
            
        # Check if email already exists
        email = self.validated_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                "error": "Email already exists"
            })
            
        # To set up the password
        account = User(**validated_data)
        # Hashes the password
        account.set_password(password)
        account.save()

        return account
            