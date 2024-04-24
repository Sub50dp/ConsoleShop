from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from utils.utils import LowercaseEmailField


class CustomUser(AbstractUser):
    email = LowercaseEmailField(unique=True, max_length=255, blank=False, null=False)
    full_name = models.CharField(max_length=255, blank=False, null=False)
    nick_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = PhoneNumberField(max_length=50, region="UA")
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)