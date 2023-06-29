from django.urls import path
from knox import views as knox_views

from . import views

urlpatterns = [
    path('login/',views.login_api),
    path('register/',views.register_api),
    path('online-users/',views.get_online_users_api),
    path('chat/start/',views.start_chat_api),
    path('logout/', knox_views.LogoutView.as_view()),
]
