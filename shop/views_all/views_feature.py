from django.db import IntegrityError
from rest_framework import status, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, get_object_or_404, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.permissions import StuffOrAdminPermission
from shop.models import Feature
from shop.serializers import FeatureSerializer


class CreateFeatureAPIView(CreateAPIView):
    serializer_class = FeatureSerializer
    permission_classes = [IsAuthenticated, StuffOrAdminPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            field, message = (list(e.detail.keys())[0], list(e.detail.values())[0][0])
            message = f"{field}: {message}"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            serializer.save()
            message = "Feature created successfully"
            status_code = status.HTTP_201_CREATED

        return Response({"message": message}, status=status_code)


class ListFeatureAPIView(ListAPIView):
    serializer_class = FeatureSerializer
    queryset = Feature.objects.all().order_by('name')
    permission_classes = [IsAuthenticated, StuffOrAdminPermission]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FeatureDeleteApiView(APIView):
    permission_classes = [IsAuthenticated, StuffOrAdminPermission]
    http_method_names = ["delete"]

    def delete(self, request, pk, *args, **kwargs):
        feature = get_object_or_404(Feature, pk=pk)
        feature.delete()
        message = "Feature deleted successfully"
        status_code = status.HTTP_200_OK
        return Response({"message": message}, status=status_code)


