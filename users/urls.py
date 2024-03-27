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
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]