from django.contrib import admin
from django.urls import path


from users import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.UserListApiView.as_view(), name='users_list',),
    path('signup/', views.CreateUserApiView.as_view(), name='signup'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('logout/', views.UserLogoutApiView.as_view(), name='logout'),
    path('delete/<int:pk>/', views.UserDeleteApiView.as_view(), name='delete'),
    path('confirm-email/<str:token>/<str:token2>/', views.UserConfirmEmailApiView.as_view(), name='confirm_email'),
    path('change_password/', views.ChangePasswordApiView.as_view(), name='change_password'),
]