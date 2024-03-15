from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.db import IntegrityError

from users.serializers import UserSerializer


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
            serializer.save()

            message = "User created successfully"
            status_code = status.HTTP_201_CREATED

        return Response({"message": message}, status=status_code)




