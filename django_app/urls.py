from django.urls import path, include, re_path
from django_app import views
from .views import SignInView, SignUpView


urlpatterns = [
    path('', views.index, name="index"),
    path('signin/', SignInView.as_view()),
    path('signup/', SignUpView.as_view()),

    

    re_path(route=r'^users/$', view=views.users, name="users"),

    re_path(route=r'^chat/(?P<sms_id>\d+)/$', view=views.chat, name="chat_id"),

    
]
