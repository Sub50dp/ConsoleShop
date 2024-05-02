from rest_framework import status, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, GenericAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import Order, OrderItem
from order.serializers import OrderSerializer, FirstStepOrderSerializer, SecondStepOrderSerializer, \
    ThirdStepOrderSerializer, OrderItemSerializer
from utils.return_cart import return_cart_for_user
from utils.return_order import return_user_order


class ListOrderApiView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff or user.is_superuser:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = self.filter_queryset(self.get_queryset()).filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateOrderApiView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = FirstStepOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        cart = return_cart_for_user(request)
        try:
            serializer.is_valid(raise_exception=True)
            shipping_address = serializer.validated_data['shipping_address']
            phone = serializer.validated_data['phone_number']
            full_name = serializer.validated_data['full_name']
            comment = serializer.validated_data['comment']
            order = Order.objects.create(shipping_address=shipping_address, phone_number=phone, full_name=full_name,
                                         comment=comment)
            for cart_item in cart.cartitem_set.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity
                )
            if request.user.is_authenticated:
                order.user = request.user
                order.save()
            else:
                order.session_key = request.session.session_key
                order.save()
            message = "Order created successfully"
            status_code = status.HTTP_201_CREATED
        except ValidationError as e:
            field, message = (list(e.detail.keys())[0], list(e.detail.values())[0][0])
            message = f"{field}: {message}"
            status_code = status.HTTP_400_BAD_REQUEST

        return Response({"message": message}, status=status_code)


class Step2UpdateOrderApiView(mixins.UpdateModelMixin, GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = SecondStepOrderSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            shipping_type = serializer.validated_data['shipping_type']
            order = return_user_order(request)
            order.shipping_type = shipping_type
            order.save()
            message = "Order updated successfully"
            status_code = status.HTTP_201_CREATED
        except ValidationError as e:
            field, message = (list(e.detail.keys())[0], list(e.detail.values())[0][0])
            message = f"{field}: {message}"
            status_code = status.HTTP_400_BAD_REQUEST

        return Response({"message": message}, status=status_code)


class Step3UpdateOrderApiView(mixins.UpdateModelMixin, GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = ThirdStepOrderSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        cart = return_cart_for_user(request)
        order = return_user_order(request)
        try:
            serializer.is_valid(raise_exception=True)
            if order.status == "completed":
                return Response({"message": "Order already paid"}, status=status.HTTP_400_BAD_REQUEST)
            cart.delete()
            order.status = "completed"
            order.save()
            message = "Order paid successfully"
            status_code = status.HTTP_200_OK
        except ValidationError as e:
            field, message = (list(e.detail.keys())[0], list(e.detail.values())[0][0])
            message = f"{field}: {message}"
            status_code = status.HTTP_400_BAD_REQUEST

        return Response({"message": message}, status=status_code)


class UserOrderApiView(RetrieveAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def retrieve(self, request, *args, **kwargs):
        order = return_user_order(request)
        if not order:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        order_serializer = OrderSerializer(order)
        order_data = order_serializer.data
        queryset = OrderItem.objects.filter(order=order)
        serializer = self.get_serializer(queryset, many=True)
        order_items_data = serializer.data
        order_items_data.insert(0, {"order": order_data})
        return Response(order_items_data, status=status.HTTP_200_OK)


class ShowOrderApiView(RetrieveAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff or user.is_superuser:
            order = Order.objects.filter(pk=kwargs['pk']).first()
        else:
            order = Order.objects.filter(pk=kwargs['pk'], user=user).first()
        if not order:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        order_serializer = OrderSerializer(order)
        order_data = order_serializer.data
        order_items = OrderItem.objects.filter(order=order)
        order_items_serializer = OrderItemSerializer(order_items, many=True)
        order_items_data = order_items_serializer.data
        order_items_data.insert(0, {"order": order_data})
        return Response(order_items_data, status=status.HTTP_200_OK)


class DeleteOrderApiView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["delete"]

    def delete(self, request, pk, *args, **kwargs):
        user = request.user
        if user.is_staff or user.is_superuser:
            order = get_object_or_404(Order, pk=pk)
        else:
            order = get_object_or_404(Order, pk=pk, user=user)
        order.delete()
        message = "Order deleted successfully"
        status_code = status.HTTP_200_OK
        return Response({"message": message}, status=status_code)