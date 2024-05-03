from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.ListCartApiView.as_view(), name="cart_list"),
    path("", views.UserCartApiView.as_view(), name="cart"),
    path("detail/<int:pk>/", views.ShowCartApiView.as_view(), name="cart_detail"),
    path("add/<int:product_pk>/", views.AddToCartApiView.as_view(), name="cart_add"),
    path("delete/<int:cart_pk>/", views.DeleteCartApiView.as_view(), name="cart_delete"),
    path("delete_item/<int:cart_item_pk>/", views.DeleteCartItemApiView.as_view(), name="cart_delete_item"),
]
