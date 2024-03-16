from django.contrib import admin
from django.urls import path


from users import views

urlpatterns = [
    path('', views.UserListApiView.as_view(), name='users_list',),
    path('signup/', views.CreateUserApiView.as_view(), name='signup'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('logout/', views.UserLogoutApiView.as_view(), name='logout'),
]