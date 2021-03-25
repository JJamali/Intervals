from django.urls import path
from .views import current_user, UserList, question, answer_check

urlpatterns = [
    path('current_user/', current_user, name='current_user'),
    path('users/', UserList.as_view()),
    path('question/', question, name='question'),
    path('answer_check/', answer_check, name='answer_check')
]
