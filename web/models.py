from django.contrib.auth.models import Permission, User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_year = models.CharField(max_length=20)
    img_url = models.CharField(max_length=400, default=" ")
    genres = models.CharField(max_length=200)
    tmdb_id = models.IntegerField()
    # precomputed data for similarity
    rating_mean = models.FloatField()
    rating_median = models.FloatField()
    num_rating = models.FloatField()
    comparable = models.BooleanField()

    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(0)])


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    tag = models.CharField(max_length=200)


# precomputed movies similarity
class Similarity(models.Model):
    first_movie = models.ForeignKey(Movie, related_name='first_movie', on_delete=models.CASCADE)
    second_movie = models.ForeignKey(Movie, related_name='second_movie', on_delete=models.CASCADE)
    similarity_score = models.FloatField()
