from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from utils.utils import LowercaseEmailField


class Contact(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = LowercaseEmailField(unique=True, max_length=255)
    phone_number = PhoneNumberField(max_length=50, region="UA", blank=True, null=True)
    message = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
