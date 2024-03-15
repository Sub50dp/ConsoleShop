from django.contrib import admin
from django.urls import path


from users import views

urlpatterns = [
    path('signup/', views.CreateUserApiView.as_view(), name='signup'),
]