from django.urls import path

from shop import views


urlpatterns = [
    path('category/create/', views.CreateCategoryAPIView.as_view(), name='create_category'),
    path('category/list/', views.ListCategoryAPIView.as_view(), name='list_category'),
    path('category/delete/<slug:cat_slug>/', views.DeleteCategoryApiView.as_view(), name='delete_category'),
    path('category/update/<slug:cat_slug>/', views.EditCategoryApiView.as_view(), name='update_category'),
    path('category/<slug:cat_slug>/', views.ListProductAPIView.as_view(), name='show_category'),
    path('feature/create/', views.CreateFeatureAPIView.as_view(), name='create_feature'),
    path('feature/list/', views.ListFeatureAPIView.as_view(), name='list_feature'),
    path('feature/delete/<int:pk>/', views.DeleteFeatureApiView.as_view(), name='delete_feature'),
    path('product/create/', views.CreateProductAPIView.as_view(), name='create_product'),
    path('product/delete/<int:pk>/', views.DeleteProductAPIView.as_view(), name='delete_product'),
    path('product/list/', views.ListProductAPIView.as_view(), name='list_product'),
    path('product/<int:pk>/', views.DetailProductAPIView.as_view(), name='detail_product'),
    path('product/update/<int:pk>/', views.EditProductApiView.as_view(), name='update_product'),
    path('rating/create/<int:product_id>/', views.CreateRatingReviewSerializer.as_view(), name='create_rating'),
    path('rating/delete/<int:pk>/', views.DeleteRatingReviewAPIView.as_view(), name='delete_rating'),
    path('rating/list/<int:product_id>/', views.ListRatingReviewAPIView.as_view(), name='list_rating'),
    path('rating/update/<int:pk>/', views.EditRatingReviewAPIView.as_view(), name='update_rating'),
]
