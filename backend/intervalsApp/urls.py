from django.urls import path
from .views import login_view, login_guest_view, logout_view, get_current_user_id, CreateGuest
from .views import UserList, UserDetail, StatsView, SettingsView
from .views import QuestionView, AnswerView

urlpatterns = [
    # authentication
    path('login/', login_view, name='login'),
    path('login_guest/', CreateGuest.as_view(), name='login_guest'),
    path('logout/', logout_view, name='logout'),
    path('current_user/', get_current_user_id, name='current_user'),
    # user data
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:id>/', UserDetail.as_view(), name='user-detail'),
    path('users/<int:id>/stats/', StatsView.as_view(), name='stats'),
    path('users/<int:id>/settings/', SettingsView.as_view(), name='settings'),
    # questions and answers
    path('users/<int:id>/question/', QuestionView.as_view(), name='question'),
    path('users/<int:id>/answer/', AnswerView.as_view(), name='answer'),
]
