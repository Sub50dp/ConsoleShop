from django.urls import path, include


from shop import views

urlpatterns = [
    path('create_category/', views.CreateCategoryAPIView.as_view(), name='create_category'),
    path('list_category/', views.ListCategoryAPIView.as_view(), name='list_category'),
    path('delete_category/<int:pk>/', views.UserDeleteApiView.as_view(), name='delete_category'),
]