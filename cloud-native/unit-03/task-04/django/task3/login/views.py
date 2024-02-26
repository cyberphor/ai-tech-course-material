import jwt
import os
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenError
from rest_framework_simplejwt.views import InvalidToken
from task3.login.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        # re-write the access token to make KrakenD happy.
        def add_kid_header(mat):
            old_encoded_jwt = jwt.decode(mat, os.getenv("PUBLIC_KEY"), algorithms=["RS256"]) 
            new_encoded_jwt = jwt.encode(old_encoded_jwt, os.getenv("PRIVATE_KEY"), algorithm="RS256", headers={"kid": "yourcoolkid"})
            return new_encoded_jwt
        
        serializer.validated_data['access']  = add_kid_header(serializer.validated_data['access'])
        serializer.validated_data['refresh'] = add_kid_header(serializer.validated_data['refresh'] )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)