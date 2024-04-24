from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from contact.models import Contact
from Console.settings import EMAIL_HOST_USER, EMAIL_ADMIN
from contact.serializers import ContactSerializer
from utils.permissions import StuffOrAdminPermission


class CreateContactAPIView(CreateAPIView):
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            message = "Your message sent successfully"
            status_code = status.HTTP_201_CREATED
            self.send_admin_email(serializer.data)
        except ValidationError as e:
            field, message = (list(e.detail.keys())[0], list(e.detail.values())[0][0])
            message = f"{field}: {message}"
            status_code = status.HTTP_400_BAD_REQUEST
        except IntegrityError:
            message = "Your already sent a message"
            status_code = status.HTTP_400_BAD_REQUEST

        return Response({"message": message}, status=status_code)

    def send_admin_email(self, contact_data):
        subject = 'New contact message'
        message = f"You have received a new message from the contact form:\n\n"

        message += f"Email: {contact_data['email']}\n"

        if contact_data.get('phone_number'):
            message += f"Phone Number: {contact_data['phone_number']}\n"

        if contact_data.get('message'):
            message += f"Message: {contact_data['message']}\n"

        from_email = EMAIL_HOST_USER
        to_email = EMAIL_ADMIN
        send_mail(subject, message, from_email, to_email)


class ListContactAPIView(ListAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all().order_by('-create_time')
    permission_classes = [IsAuthenticated, StuffOrAdminPermission]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetailContactApiView(RetrieveAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    permission_classes = [IsAuthenticated, StuffOrAdminPermission]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response({"message": "Contact not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteContactApiView(APIView):
    permission_classes = [IsAuthenticated, StuffOrAdminPermission]
    http_method_names = ["delete"]

    def delete(self, request, pk, *args, **kwargs):
        contact = get_object_or_404(Contact, id=pk)
        contact.delete()
        return Response({"message": "Contact deleted successfully"}, status=status.HTTP_200_OK)