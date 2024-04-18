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
from shop.models import Category, Product, Feature, ProductRating
from shop.serializers import CreateProductSerializer, ProductSerializer, EditProductSerializer, FeatureSerializer, \
    CreateRatingSerializer, EditRatingSerializer
from utils.permissions import StuffOrAdminPermission, OwnOrAdminPermission, CustomUnauthorizedException


class CreateRatingReviewSerializer(CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    queryset = ProductRating.objects.all()
    serializer_class = CreateRatingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['product_id'])
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(product=product, user=request.user)
            message = "Review created successfully"
            status_code = status.HTTP_201_CREATED
        except ValidationError as e:
            field, message = (list(e.detail.keys())[0], list(e.detail.values())[0][0])
            message = f"{field}: {message}"
            status_code = status.HTTP_400_BAD_REQUEST
        except IntegrityError:
            message = "You already left a review for this product"
            status_code = status.HTTP_400_BAD_REQUEST

        return Response({"message": message}, status=status_code)


class DeleteRatingReviewAPIView(APIView):

    permission_classes = [IsAuthenticated]
    http_method_names = ["delete"]

    def delete(self, request, pk, *args, **kwargs):
        if (not request.user.is_staff and not request.user.is_superuser and
                not request.user.id == ProductRating.objects.get(id=pk).user.id):
            raise CustomUnauthorizedException
        rating = get_object_or_404(ProductRating, id=pk)
        rating.delete()
        message = "Review deleted successfully"
        status_code = status.HTTP_200_OK
        return Response({"message": message}, status=status_code)


class ListRatingReviewAPIView(ListAPIView):
    serializer_class = CreateRatingSerializer

    def get_queryset(self, *args, **kwargs):
        return ProductRating.objects.filter(product=self.kwargs['product_id'])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EditRatingReviewAPIView(GenericAPIView, mixins.UpdateModelMixin):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = EditRatingSerializer
    permission_classes = [IsAuthenticated]
    queryset = ProductRating.objects.all()

    def put(self, request, pk, *args, **kwargs):
        partial = True
        rating = get_object_or_404(ProductRating, id=pk)
        if (not request.user.is_staff and not request.user.is_superuser and
                not request.user.id == rating.user.id):
            raise CustomUnauthorizedException
        serializer = self.get_serializer(rating, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            message = "Review updated successfully"
            status_code = status.HTTP_200_OK
        except ValidationError as e:
            field, message = (list(e.detail.keys())[0], list(e.detail.values())[0][0])
            message = f"{field}: {message}"
            status_code = status.HTTP_400_BAD_REQUEST

        return Response({"message": message}, status=status_code)