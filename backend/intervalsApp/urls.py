from django.urls import path
from .views import current_user, UserList, question, answer_check, login_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('current_user/', current_user, name='current_user'),
    path('users/', UserList.as_view()),
    path('question/', question, name='question'),
    path('answer_check/', answer_check, name='answer_check')
]
