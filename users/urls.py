from django.urls import path, include


from users import views

urlpatterns = [
    path('', views.UserListApiView.as_view(), name='users_list',),
    path('signup/', views.CreateUserApiView.as_view(), name='signup'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('logout/', views.UserLogoutApiView.as_view(), name='logout'),
    path('delete/<int:pk>/', views.UserDeleteApiView.as_view(), name='delete'),
    path('confirm-email/<str:token>/<str:token2>/', views.UserConfirmEmailApiView.as_view(), name='confirm_email'),
    path('change_password/', views.ChangePasswordApiView.as_view(), name='change_password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]