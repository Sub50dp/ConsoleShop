from rest_framework import serializers


def validate_password(value):

    if len(value) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters long")

    if not any(char.isdigit() for char in value):
        raise serializers.ValidationError("Password must contain at least one digit")

    if not any(char.isalpha() for char in value):
        raise serializers.ValidationError("Password must contain at least one letter")

    return value
