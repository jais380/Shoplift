from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from account.api.serializers import RegistrationSerializers



@api_view(['POST',])
def Register(request):

    if request.method == 'POST':
        serializers = RegistrationSerializers(data=request.data)

        data = {}

        if serializers.is_valid():
            account = serializers.save()

            data['response'] = "Registration Successful"
            data['username'] = account.username
            data['email'] = account.email

            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

        else:
            data = serializers.errors
        
        return Response(data)
