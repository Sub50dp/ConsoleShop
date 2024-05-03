from rest_framework import serializers


def validate_password(value):

    if len(value) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters long")

    if not any(char.isdigit() for char in value):
        raise serializers.ValidationError("Password must contain at least one digit")

    if not any(char.isalpha() for char in value):
        raise serializers.ValidationError("Password must contain at least one letter")

    return value


def validate_card_number(value):
    cleaned_value = value.replace(" ", "").replace("-", "")

    if not cleaned_value.isdigit():
        raise serializers.ValidationError("Card number must contain only digits.")

    if len(cleaned_value) < 13 or len(cleaned_value) > 19:
        raise serializers.ValidationError("Invalid card number length.")

    # Luhn algorithm
    # check_sum = 0
    # num_digits = len(cleaned_value)
    # even_digits = False
    #
    # for i in range(num_digits - 1, -1, -1):
    #     digit = int(cleaned_value[i])
    #
    #     if even_digits:
    #         digit *= 2
    #
    #         if digit > 9:
    #             digit -= 9
    #
    #     check_sum += digit
    #     even_digits = not even_digits
    #
    # if check_sum % 10 != 0:
    #     raise serializers.ValidationError("Invalid card number.")

    return value


def validate_card_expiry(value):
    if not value:
        raise serializers.ValidationError("Card expiry date is required.")

    try:
        from datetime import datetime
        expiry_date = datetime.strptime(value, '%m/%y')
    except ValueError:
        raise serializers.ValidationError("Invalid expiry date format. Use MM/YY.")

    current_date = datetime.now()
    if expiry_date < current_date:
        raise serializers.ValidationError("Card has expired.")

    return value


def validate_card_cvc(value):
    if not value:
        raise serializers.ValidationError("Card CVC is required.")

    if not value.isdigit():
        raise serializers.ValidationError("Card CVC must contain only digits.")

    if len(value) < 3 or len(value) > 4:
        raise serializers.ValidationError("Invalid CVC/CVV length. Must be 3 or 4 digits.")

    return value
