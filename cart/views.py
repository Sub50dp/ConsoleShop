from rest_framework import status, mixins
from rest_framework.generics import ListAPIView, get_object_or_404, GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Product
from utils.permissions import StuffOrAdminPermission

from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartSerializer, AddToCartSerializer
from utils.return_cart import return_cart_for_user


class UserCartApiView(RetrieveAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        cart = return_cart_for_user(request)
        queryset = queryset.filter(cart=cart)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShowCartApiView(RetrieveAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, StuffOrAdminPermission]

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        cart = Cart.objects.filter(pk=kwargs['pk']).first()
        if not cart:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        queryset = queryset.filter(cart=cart)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListCartApiView(ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, StuffOrAdminPermission]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddToCartApiView(GenericAPIView, mixins.UpdateModelMixin):
    queryset = CartItem.objects.all()
    serializer_class = AddToCartSerializer

    def put(self, request, product_pk, *args, **kwargs):
        cart = return_cart_for_user(request)
        product = get_object_or_404(Product, pk=product_pk)
        quantity = request.data.get('quantity', 1)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteCartApiView(APIView):
    permission_classes = [IsAuthenticated, StuffOrAdminPermission]
    http_method_names = ["delete"]

    def delete(self, request, cart_pk, *args, **kwargs):
        cart = get_object_or_404(Cart, pk=cart_pk)
        cart.delete()
        message = "Cart deleted successfully"
        status_code = status.HTTP_200_OK
        return Response({"message": message}, status=status_code)


class DeleteCartItemApiView(APIView):
    http_method_names = ["delete"]

    def delete(self, request, cart_item_pk, *args, **kwargs):
        cart = return_cart_for_user(request)
        cart_item = CartItem.objects.filter(pk=cart_item_pk, cart=cart).first()
        if not cart_item:
            message = "Cart item not found"
            status_code = status.HTTP_404_NOT_FOUND
        else:
            cart_item.delete()
            message = "Cart item deleted successfully"
            status_code = status.HTTP_200_OK
        return Response({"message": message}, status=status_code)