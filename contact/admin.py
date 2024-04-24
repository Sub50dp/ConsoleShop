from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "phone_number")
    fields = ("email", "phone_number", "message", "create_time", "first_name", "last_name")
    readonly_fields = ("create_time",)
