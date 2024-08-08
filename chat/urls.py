from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('user-list/', views.get_user_list_with_unread_count, name='user_list'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('messages/<int:user_id>/', views.get_messages, name='get_messages'),
    path('send_message/', views.send_message, name='send_message'),
]