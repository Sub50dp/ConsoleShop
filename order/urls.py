from django.urls import path

from order import views


urlpatterns = [
    path('', views.UserOrderApiView.as_view(), name='order'),
    path('list/', views.ListOrderApiView.as_view(), name='list_order'),
    path('create/', views.CreateOrderApiView.as_view(), name='create_order'),
    path('add_shipping_type/', views.Step2UpdateOrderApiView.as_view(), name='add_shipping_type'),
    path('pay/', views.Step3UpdateOrderApiView.as_view(), name='pay'),
    path('detail/<int:pk>/', views.ShowOrderApiView.as_view(), name='detail_order'),
    path('delete/<int:pk>/', views.DeleteOrderApiView.as_view(), name='delete_order'),
]
