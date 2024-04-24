from django.db import models


class LowercaseEmailField(models.EmailField):
    """
    A custom EmailField that converts email addresses to lowercase.
    """

    def get_prep_value(self, value):
        return value.lower()