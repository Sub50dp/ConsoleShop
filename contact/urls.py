from django.urls import path

from contact import views


urlpatterns = [
    path('create/', views.CreateContactAPIView.as_view(), name='contact_create'),
    path('list/', views.ListContactAPIView.as_view(), name='contact_list'),
    path('detail/<int:pk>/', views.DetailContactApiView.as_view(), name='contact_detail'),
    path('delete/<int:pk>/', views.DeleteContactApiView.as_view(), name='contact_delete'),
]