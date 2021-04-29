from django.urls import path
from .views import current_user, UserList, question, answer_check, login_view, logout_view, global_stats, update_settings

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('current_user/', current_user, name='current_user'),
    path('users/', UserList.as_view()),
    path('question/', question, name='question'),
    path('answer_check/', answer_check, name='answer_check'),
    path('global_stats/', global_stats, name='global_stats'),
    path('update_settings/', update_settings, name='update_settings')
]
