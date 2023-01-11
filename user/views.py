from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.authenticate import Authenticate
from user.models import User
from user.modules import hash_password
from user.serializers import UserSerializer, UserDeserializer, LoginDeserializer, UpdateUserDeserializer


class GetUsers(APIView):

    def get(self, request):
        users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)


class GetUserDetail(APIView):

    def get(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if not user:
            return Response({"User error": "User not fount"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateUsers(APIView):

    def post(self, request):
        data = UserDeserializer(data=request.data)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        # Create new user
        # Check unique username
        count = User.objects.filter(username=data.validated_data['username']).count()
        if count > 0:
            return Response({"Username error": "Username must be unique"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(
            first_name=data.validated_data['first_name'],
            last_name=data.validated_data['last_name'],
            username=data.validated_data['username'],
            password=hash_password(data.validated_data['password']),
        )
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)


class DeleteUser(APIView):

    def delete(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if not user:
            return Response({"User error": "User not fount"}, status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response({"Result": "User deleted"}, status=status.HTTP_200_OK)


class Login(APIView):

    def post(self, request):
        data = LoginDeserializer(data=request.data)
        if not data.is_valid():
            return Response({"Error": "Username and Password are required!"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(
            username=data.validated_data['username'],
            password=hash_password(data.validated_data['password'])
        ).first()
        if not user:
            return Response({"Error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        authenticate = Authenticate()
        token = authenticate.create_access_token(user.id)
        user_serializer = UserSerializer(user, many=False, context={'token': token})
        return Response(user_serializer.data, status=status.HTTP_200_OK)


class UpdateUser(APIView):

    def put(self, request):
        authenticate = Authenticate()
        user = authenticate.get_user_by_request(request)
        if not user or user is None:
            return Response({"Error": "Please login"}, status=status.HTTP_401_UNAUTHORIZED)

        data = UpdateUserDeserializer(data=request.data)
        if not data.is_valid():
            return Response({"Error": "First name and Last name are required!"}, status=status.HTTP_400_BAD_REQUEST)

        user.first_name = data.validated_data['first_name']
        user.last_name = data.validated_data['last_name']
        user.save()

        update_user_serializer = UserSerializer(user, many=False)

        return Response(update_user_serializer.data, status=status.HTTP_200_OK)
