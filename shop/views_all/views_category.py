from django.db import IntegrityError
from rest_framework import status, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, get_object_or_404, GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Category, Product
from shop.serializers import CategorySerializer, ProductSerializer
from utils.permissions import StuffOrAdminPermission


class CreateCategoryAPIView(CreateAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, StuffOrAdminPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

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
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_slug = self.kwargs['cat_slug']
        return Product.objects.filter(category__slug=category_slug, available=True).order_by('name')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryDeleteApiView(APIView):

    permission_classes = [IsAuthenticated, StuffOrAdminPermission]
    http_method_names = ["delete"]

    def delete(self, request, cat_slug, *args, **kwargs):
        category = get_object_or_404(Category, slug=cat_slug)
        category.delete()
        message = "Category deleted successfully"
        status_code = status.HTTP_200_OK
        return Response({"message": message}, status=status_code)


class CategoryEditApiView(mixins.UpdateModelMixin, GenericAPIView):

    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, StuffOrAdminPermission]
    serializer_class = CategorySerializer

    def put(self, request, cat_slug, *args, **kwargs):
        partial = True
        category = get_object_or_404(Category, slug=cat_slug)
        serializer = self.get_serializer(category, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            field, message = (list(e.detail.keys())[0], list(e.detail.values())[0][0])
            message = f"{field}: {message}"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            serializer.save()
            message = "Category updated successfully"
            status_code = status.HTTP_200_OK
        return Response({"message": message}, status=status_code)