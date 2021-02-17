from django.urls import path
from intervalsApp import views

urlpatterns = [
    path('create_user/', views.create_user),

]