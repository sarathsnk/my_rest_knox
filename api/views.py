from django.contrib.auth.models import User
from rest_framework import generics, permissions
from knox.models import AuthToken
from rest_framework.response import Response
from .serializers import RegisterSerializer

from rest_framework import status
from django.contrib.auth import authenticate

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer   # ✅ ADD THIS
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "User already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(username=username, password=password)
        token = AuthToken.objects.create(user)[1]

        return Response({
            "user": user.username,
            "token": token
        })

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import LoginSerializer

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer   # ✅ REQUIRED
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        return Response({
            "user": user.username,
            "token": AuthToken.objects.create(user)[1]
        })
