from django.shortcuts import render
from rest_framework import generics, status
from .serializers import UserSerializer, CreateUserSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUserView(APIView):
    serializer_class = CreateUserSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id = serializer.data.get("id")
            code = serializer.data.get("code")
            host = self.request.session.session_key
            queryset = User.objects.filter(host=host)
            if queryset.exists():
                user = queryset[0]
                user.code = code
                user.id = id
                user.save(update_fields=["id", "code"])
            else:
                user = User(host=host, id=id, code=code)

            return Response(UserSerializer(user).data, status=status.HTTP_202)
