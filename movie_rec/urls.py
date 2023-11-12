from django.contrib import admin
from django.urls import path

from web import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('signup/', views.signUp, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('recommend/', views.recommend, name='recommend'),
    path('user', views.user_ratings, name='userPage'),
    path('update-rating/<int:movie_id>/', views.update_rating, name='update_rating'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('about-us/', views.about_us, name='about_us'),
    # path('ratemovies/', views.rateMovies, name='ratemovies')
]

handler404 = "web.views.handle_not_found"
handler500 = "web.views.handle_server_error"