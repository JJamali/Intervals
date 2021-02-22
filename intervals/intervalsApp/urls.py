from django.urls import path
from intervalsApp import views
from .views import UserList

urlpatterns = [
    path('create_user/', views.create_user),
    path('users/', UserList.as_view())
]
