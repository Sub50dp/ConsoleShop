from django.contrib.auth import get_user_model, logout, authenticate, login
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, filters, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework.views import APIView

from users.serializers import UserSerializer, LoginSerializer
from users.swagger_schemas import delete_user_response_schema
from utils.permissions import OwnOrAdminPermission, StuffOrAdminPermission


class CreateUserApiView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            field, message = (list(e.detail.keys())[0], list(e.detail.values())[0][0])
            message = f"{field}: {message}"
            status_code = status.HTTP_400_BAD_REQUEST
        except IntegrityError:
            message = "This email is already in use"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            validated_data = serializer.validated_data
            password = validated_data.get("password")
            hashed_password = make_password(password)
            validated_data["password"] = hashed_password
            validated_data["is_active"] = False
            serializer.save()

            message = "User created successfully"
            status_code = status.HTTP_201_CREATED

        return Response({"message": message}, status=status_code)


class UserListApiView(ListAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.IsAuthenticated, StuffOrAdminPermission]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["username", "email"]
    ordering_fields = "__all__"


class UserLoginApiView(CreateAPIView):
    serializer_class = LoginSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [~permissions.IsAuthenticated]

    def post(self, request: Request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            field, message = (list(e.detail.keys())[0], list(e.detail.values())[0][0])
            message = f"{field}: {message}"
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": message}, status=status_code)

        data = serializer.validated_data

        try:
            user = authenticate(request, username=data["email"], password=data["password"])
        except Exception as e:
            message = "An error occurred during authentication"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            if user is not None:
                login(request, user)
                message = "Login successful"
                status_code = status.HTTP_200_OK
            else:
                message = "Incorrect email or password"
                status_code = status.HTTP_403_FORBIDDEN

        return Response({"message": message}, status=status_code)


class UserLogoutApiView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        message = "Logout successful"
        status_code = status.HTTP_200_OK

        return Response({"message": message}, status=status_code)


class UserDeleteApiView(APIView):

    permission_classes = [permissions.IsAuthenticated, OwnOrAdminPermission]
    http_method_names = ["delete"]

    @swagger_auto_schema(
        responses=delete_user_response_schema,
    )
    def delete(self, request, pk, *args, **kwargs):
        try:
            user = get_user_model().objects.get(id=pk)
            user.delete()
            message = "User deleted successfully"
            status_code = status.HTTP_200_OK
        except get_user_model().DoesNotExist:
            message = "User not found"
            status_code = status.HTTP_404_NOT_FOUND

        return Response({"message": message}, status=status_code)
