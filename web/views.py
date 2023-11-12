import pprint

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import Http404
from .models import Movie, Rating, Tag
from django.contrib import messages
from .forms import UserForm
from tmdbv3api import TMDb
from tmdbv3api import Movie as TMDbMovie
from django.contrib.auth import authenticate, login as auth_login

import requests
import csv
import requests
from django.db.models import Case, When
# from .recommendation import Myrecommend
import numpy as np
import pandas as pd

from .scripts.recommendation import Myrecommend

url = "https://api.themoviedb.org/3/"
token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmYjk3MWVlZDQ4ODBlZDM0ZDIwMGRhMzVhOGE3Nzk0MiIsInN1YiI6IjY1MzNlMjY2YTBiZTI4MDExY2JiMTJjMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.R2Cv8H1kKd3flr508BP1ZPdogZNKzTvmLLf1ExOHQu4"


# List view
def index(request):

    # Get the search query from the request
    search_query = request.GET.get('q', '')

    # Retrieve all movies or filter by search query
    if search_query:
        movies = Movie.objects.filter(title__icontains=search_query).order_by('id')
    else:
        movies = Movie.objects.all().order_by('id')

    # Number of movies per page
    items_per_page = 30
    paginator = Paginator(movies, items_per_page)

    # Get the current page number from the request
    page = request.GET.get('page', 1)

    try:
        movies_page = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, show the first page
        movies_page = paginator.page(1)
    except EmptyPage:
        # If the page is out of range (e.g., 9999), show the last page
        movies_page = paginator.page(paginator.num_pages)

    print(movies_page)
    return render(request, 'web/list.html', {'movies': movies_page})

# detail view
def detail(request, movie_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    movie = get_object_or_404(Movie, id=movie_id)
    ratings = Rating.objects.filter(movie=movie)[:20]
    tags = Tag.objects.filter(movie_id=movie_id)
    genres = movie.genres.split('|')

    # Fetch additional movie details from TMDb API
    tmdb_details = requests.get("https://api.themoviedb.org/3/movie/" + str(movie.tmdb_id) + "?language=en-US",
                                headers={
                                    "accept": "application/json",
                                    "Authorization": "Bearer " + token
                                },

                                )
    tmdb_credits = requests.get("https://api.themoviedb.org/3/movie/" + str(movie.tmdb_id) + "/credits?language=en-US",
                                headers={
                                    "accept": "application/json",
                                    "Authorization": "Bearer " + token
                                }
                                )

    tmdb_credits_data = tmdb_credits.json()
    tmdb_details_data = tmdb_details.json()


    try:
        pprint.pprint(tmdb_credits_data['cast'])
        print(movie.tmdb_id)
        pprint.pprint(tmdb_details_data)
    except UnicodeEncodeError as e:
        print(f"UnicodeEncodeError: {e}")
    # print(tmdb_details)

    # for rating
    if request.method == "POST":
        rate = request.POST['rating']
        ratingObject = Rating()
        ratingObject.user = request.user
        ratingObject.movie = movie
        ratingObject.rating = rate
        ratingObject.save()
        messages.success(request, "Your Rating is submitted")
        return redirect("index")
    return render(request, 'web/detail.html', {'movie': movie,
                                               'tmdb_details': tmdb_details_data,
                                               'ratings': ratings,
                                               'genres': genres,
                                               'tags': tags,
                                               'credits': tmdb_credits_data['cast']
                                               })


# Register user
def signUp(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("index")
    context = {
        'form': form
    }
    return render(request, 'web/signUp.html', context)


# Login User
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect("index")
            else:
                return render(request, 'web/login.html', {'error_message': 'Your account disable'})
        else:
            return render(request, 'web/login.html', {'error_message': 'Invalid Login'})
    return render(request, 'web/login.html')


# Logout user
def Logout(request):
    logout(request)
    return redirect("login")


def recommend(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    df = pd.DataFrame(list(Rating.objects.all().values()))
    nu = df.user_id.unique().shape[0]
    current_user_id = request.user.id

    # if new user not rated any movie
    if current_user_id > nu:
        movie = Movie.objects.get(id=15)
        q = Rating(user=request.user, movie=movie, rating=0)
        q.save()

    print("Current user id: ", current_user_id)
    prediction_matrix, Ymean = Myrecommend()
    my_predictions = prediction_matrix[:, current_user_id - 1] + Ymean.flatten()
    pred_idxs_sorted = np.argsort(my_predictions)
    pred_idxs_sorted[:] = pred_idxs_sorted[::-1]
    pred_idxs_sorted = pred_idxs_sorted + 1
    print(pred_idxs_sorted)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pred_idxs_sorted)])
    movie_list = list(Movie.objects.filter(id__in=pred_idxs_sorted).order_by(preserved)[:10])

    return render(request, 'web/recommend.html', {'movie_list': movie_list})


def handle_not_found(request, exception):
    return render(request, 'web/not-found.html')


def handle_server_error(request, *args, **argv):
    return render(request, 'web/server-error.html')

def user_ratings(request):
    user_ratings = Rating.objects.filter(user=request.user).select_related('movie')
    context = {'user_ratings': user_ratings}
    return render(request, 'web/user-page.html', context)

def update_rating(request, movie_id):
    if request.method == 'POST':
        new_rating = request.POST.get('rating')

        # Validate the rating (e.g., check if it's a valid number)
        try:
            new_rating = int(new_rating)
        except ValueError:
            messages.error(request, 'Invalid rating. Please select a valid rating.')
            return redirect('userPage')

        # Assuming you have a UserRating model with a ForeignKey to Movie
        user_rating, created = Rating.objects.get_or_create(user=request.user, movie_id=movie_id)
        user_rating.rating = new_rating
        user_rating.save()

        messages.success(request, 'Rating updated successfully.')
        return redirect('userPage')

    return redirect('userPage')  # Redirect if it's not a POST request

def contact_us(request):
    return render(request, 'web/contact_us.html')

def about_us(request):
    return render(request, 'web/about_us.html')