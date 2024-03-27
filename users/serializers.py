from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from utils.validators import validate_password


class UserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(max_length=50, region="UA", required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'phone_number', 'full_name', 'nick_name', 'address', 'password', 'password_2',]
        extra_kwargs = {
                        'email': {'required': True},
                        'full_name': {'required': True},
                        }

    def validate(self, data):
        password = data.get('password')
        password_2 = data.get('password_2')

        if password and password_2 and password != password_2:
            raise ValidationError("Passwords do not match")

        return data

    def create(self, validated_data):
        validated_data.pop('password_2')  # Remove password_2 from validated_data
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
