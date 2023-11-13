from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# ... the rest of your URLconf here ...


from web import views

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('icons/film-tape.gif'))),


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
urlpatterns += staticfiles_urlpatterns()

handler404 = "web.views.handle_not_found"
handler500 = "web.views.handle_server_error"

"""
    path('add-user.gif', RedirectView.as_view(url=staticfiles_storage.url('icons/add-user.gif'))),
    path('agenda.gif', RedirectView.as_view(url=staticfiles_storage.url('icons/agenda.gif'))),
    path('directors-chair.gif', RedirectView.as_view(url=staticfiles_storage.url('icons/directors-chair.gif'))),
    path('facebook-app-symbol.png', RedirectView.as_view(url=staticfiles_storage.url('icons/facebook-app-symbol.png'))),
    path('film-reel.gif', RedirectView.as_view(url=staticfiles_storage.url('icons/film-reel.gif'))),
    path('film-tape.gif', RedirectView.as_view(url=staticfiles_storage.url('icons/film-tape.gif'))),
    path('heart.gif', RedirectView.as_view(url=staticfiles_storage.url('icons/heart.gif'))),
    path('knight.gif', RedirectView.as_view(url=staticfiles_storage.url('icons/knight.gif'))),
    path('line-bars.gif', RedirectView.as_view(url=staticfiles_storage.url('icons/line-bars.gif'))),
    path('linkedin.png', RedirectView.as_view(url=staticfiles_storage.url('icons/linkedin.png'))),
    path('phishing.gif', RedirectView.as_view(url=staticfiles_storage.url('icons/phishing.gif'))),
    path('red-carpet.gif', RedirectView.as_view(url=staticfiles_storage.url('icons/red-carpet.gif'))),
    path('twitter.png', RedirectView.as_view(url=staticfiles_storage.url('icons/twitter.png'))),
"""