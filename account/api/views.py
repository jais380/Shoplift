from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_spectacular.utils import extend_schema

from account.api.serializers import RegistrationSerializers

class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({
                "error": "Refresh Token is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)

            if token['user_id'] != request.user.id:
                return Response({
                    "error": "Token does not belong to the user"
                }, status=status.HTTP_403_FORBIDDEN)
            
            token.blacklist()

            return Response({
                "message": "Logout successful"
            }, status=status.HTTP_205_RESET_CONTENT)
        
        except TokenError:
            return Response({
                "error": "Token is expired or invalid"
            }, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(APIView):

    @extend_schema(
    request=RegistrationSerializers,
    responses=RegistrationSerializers,
    )
    def post(self, request):
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

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
