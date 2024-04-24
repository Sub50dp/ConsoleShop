from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from contact.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(max_length=50, region="UA", required=False)

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'message']
        extra_kwargs = {
            'message': {'required': False},
        }