from django.db import IntegrityError
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins, filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, get_object_or_404, GenericAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.filters import ProductFilter
from shop.models import Category, Product, Feature
from shop.serializers import CreateProductSerializer, ProductSerializer
from utils.permissions import StuffOrAdminPermission


class CreateProductAPIView(CreateAPIView):
    queryset = Product.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CreateProductSerializer
    permission_classes = [IsAuthenticated, StuffOrAdminPermission]

    def create(self, request, *args, **kwargs):
        if 'features' in request.data:
            features_list = request.data['features'].split(',')
            request.data._mutable = True
            request.data.pop('features')
            request.data._mutable = False
        else:
            features_list = None
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            field, message = (list(e.detail.keys())[0], list(e.detail.values())[0][0])
            message = f"{field}: {message}"
            status_code = status.HTTP_400_BAD_REQUEST
        except IntegrityError:
            message = "This product is already in use"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            product = serializer.create(serializer.validated_data)
            if features_list:
                for feature_id in features_list:
                    feature = get_object_or_404(Feature, id=feature_id)
                    product.features.add(feature)
            product.save()
            message = "Product created successfully"
            status_code = status.HTTP_201_CREATED

        return Response({"message": message}, status=status_code)


class DeleteProductAPIView(APIView):

    permission_classes = [IsAuthenticated, StuffOrAdminPermission]
    http_method_names = ["delete"]

    def delete(self, request, prod_slug, *args, **kwargs):
        product = get_object_or_404(Product, slug=prod_slug)
        product.delete()
        message = "Product deleted successfully"
        status_code = status.HTTP_200_OK
        return Response({"message": message}, status=status_code)


class ListProductAPIView(ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["name", "category__name", "brand"]
    ordering_fields = "__all__"
    filterset_class = ProductFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if 'cat_slug' in self.kwargs:
            category_slug = self.kwargs['cat_slug']
            queryset = queryset.filter(category__slug=category_slug)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetailProductAPIView(RetrieveAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)