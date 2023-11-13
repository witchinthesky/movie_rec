from web.models import Movie, Similarity, Rating
import pprint


# Load similar movies from database based on similarity score
def load_identical_movies(movie, n):
    print(movie)
    similarities = Similarity.objects.filter(
        first_movie=movie.id,
    ).exclude(
        second_movie__id=movie.id
    ).order_by('-similarity_score')

    similar_movies = []
    print("SIMILARITY")
    for similarity in similarities[:n]:
#        print(similarity.second_movie.id)
        similar_movie = similarity.second_movie_id
        similar_movies.append(similar_movie)
    return similar_movies


def get_similar_movies(movies):
    all_similar_movies = []
    for movie in movies:
        all_similar_movies.extend(load_identical_movies(movie, 20))
        print(all_similar_movies)
    # movie_ids = [movie_id for movie_title, movie_id in all_similar_movies]
    return Movie.objects.filter(id__in=all_similar_movies)


# Filter similar movies from the already liked movies
def exclude_liked_movies(similar_unliked_movies, similar_liked_movies, reviewed_movies):

    similar_liked_ids = similar_liked_movies.values_list('id', flat=True)
    reviewed_movies_ids = reviewed_movies.values_list('id', flat=True)

    for i in similar_liked_movies:
        print(i)
    # exclude already watched movies
    similar_liked_movies = similar_liked_movies.exclude(id__in=reviewed_movies_ids)
    print("before filtering".upper())
    for i in similar_liked_movies:
        print(similar_liked_movies)
    similar_unliked_movies = similar_unliked_movies.exclude(id__in=reviewed_movies_ids)

    unliked = similar_unliked_movies.exclude(id__in=similar_liked_ids)[:24]
    liked = similar_liked_movies[:24]
    return liked, unliked


# Load recommendations based on liked and unliked movies
def load_recommendations(user):

    liked_movies = Movie.objects.filter(
        rating__user_id=user.id,
        rating__rating__gt=2,
        #comparable=True
    )

    similar_liked_movies = get_similar_movies(liked_movies)
    similar_liked_movies.order_by('?')

    unliked_movies = Movie.objects.filter(
        rating__user_id=user.id,
        rating__rating__lt=3,
        #comparable=True
    )

    similar_unliked_movies = get_similar_movies(unliked_movies)
    similar_unliked_movies.order_by('-rating_mean')

    reviewed_movies = Movie.objects.filter(
        rating__user=user.id,
    )

    liked, unliked = exclude_liked_movies(similar_unliked_movies, similar_liked_movies, reviewed_movies)
    return liked, unliked
