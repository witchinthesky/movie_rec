from django.contrib import admin
from django.urls import path

from web import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('signup/', views.signUp, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('recommend/', views.recommend, name='recommend')
]

handler404 = "web.views.handle_not_found"
handler500 = "web.views.handle_server_error"