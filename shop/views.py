from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from shop.models import Category
from shop.serializers import CategorySerializer
from utils.permissions import StuffOrAdminPermission


class CreateCategoryAPIView(CreateAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [StuffOrAdminPermission]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        from django.db import IntegrityError
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            field, message = (list(e.detail.keys())[0], list(e.detail.values())[0][0])
            message = f"{field}: {message}"
            status_code = status.HTTP_400_BAD_REQUEST
        except IntegrityError:
            message = "This category is already in use"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            serializer.save()
            message = "Category created successfully"
            status_code = status.HTTP_201_CREATED

        return Response({"message": message}, status=status_code)


class ListCategoryAPIView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('name')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShowCategoryAPIView(ListAPIView):
    pass