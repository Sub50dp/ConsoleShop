from django.db import IntegrityError
from rest_framework import status, mixins
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.generics import ListAPIView, CreateAPIView, get_object_or_404, GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Category, Product, Feature
from shop.serializers import CreateProductSerializer
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
