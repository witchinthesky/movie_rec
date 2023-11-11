from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import Http404
from .models import Movie, Rating
from django.contrib import messages
from .forms import UserForm
import requests
import csv
import requests
from django.db.models import Case, When
# from .recommendation import Myrecommend
import numpy as np
import pandas as pd

# for recommendation
# def recommend(request):
# if not request.user.is_authenticated:
#	return redirect("login")
# if not request.user.is_active:
#	raise Http404
# df=pd.DataFrame(list(Rating.objects.all().values()))
# nu=df.user_id.unique().shape[0]
# current_user_id= request.user.id
# if new user not rated any movie
# if current_user_id>nu:
# movie=Movie.objects.get(id=15)
# q=Rating(user=request.user,movie=movie,rating=0)
# q.save()

# print("Current user id: ",current_user_id)
# prediction_matrix,Ymean = Myrecommend()
# my_predictions = prediction_matrix[:,current_user_id-1]+Ymean.flatten()
# pred_idxs_sorted = np.argsort(my_predictions)
# pred_idxs_sorted[:] = pred_idxs_sorted[::-1]
# pred_idxs_sorted=pred_idxs_sorted+1
# print(pred_idxs_sorted)
# preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pred_idxs_sorted)])
# movie_list=list(Movie.objects.filter(id__in = pred_idxs_sorted,).order_by(preserved)[:10])
# return render(request,'web/recommend.html',{'movie_list':movie_list})

url = "https://api.themoviedb.org/3/"
token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhNmIzZGViZmUzYWEyODI5NzQyZTBkMTQwZDRmMTdiNiIsInN1YiI6IjY1MzNlMjY2YTBiZTI4MDExY2JiMTJjMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.TUTRC6tXJ4HG1Oyvw6CiLbe6jwUY3aNoOEeiRiy0p4Q"


# List view
def index(request):
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

''' def index(request, ind):
    # Convert ind to an integer (if it's not already) and ensure it's non-negative
    ind = max(int(ind), 0) * 20

    # Retrieve 20 items from the database starting from the specified index
    movies = Movie.objects.all()[ind:ind + 20]

    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(Q(title__icontains=query)).distinct()[ind:ind + 20]
        return render(request, 'web/list.html', dict(movies=movies))

    return render(request, 'web/list.html', dict(movies=movies))
'''

# detail view
def detail(request, movie_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    movies = get_object_or_404(Movie, id=movie_id)
    # for rating
    if request.method == "POST":
        rate = request.POST['rating']
        ratingObject = Rating()
        ratingObject.user = request.user
        ratingObject.movie = movies
        ratingObject.rating = rate
        ratingObject.save()
        messages.success(request, "Your Rating is submited ")
        return redirect("index")
    return render(request, 'web/detail.html', dict(movies=movies))


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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
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
    return None


def handle_not_found(request, exception):
    return render(request, 'web/not-found.html')


def handle_server_error(request, *args, **argv):
    return render(request, 'web/server-error.html')
