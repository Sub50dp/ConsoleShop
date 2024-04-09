from django.urls import path


from shop import views

urlpatterns = [
    path('create_category/', views.CreateCategoryAPIView.as_view(), name='create_category'),
    path('list_category/', views.ListCategoryAPIView.as_view(), name='list_category'),
    path('delete_category/<int:pk>/', views.CategoryDeleteApiView.as_view(), name='delete_category'),
    path('update_category/<int:pk>/', views.CategoryEditApiView.as_view(), name='update_category'),
    path('show_category/<int:pk>/', views.ShowCategoryAPIView.as_view(), name='show_category'),
]