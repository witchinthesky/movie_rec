import csv

from django.contrib.sites import requests



TMDB_API_KEY = 'a6b3debfe3aa2829742e0d140d4f17b6'

help = 'Fetch movie details from TMDb and extract image URL'

input_csv_file = "C:\\Users\\maria\\PycharmProjects\\movie_rec\\web\\link.csv"
output_csv_file = "C:\\Users\\maria\\PycharmProjects\\movie_rec\\web\\output.csv"

with open(input_csv_file, 'r') as input_csv, open(output_csv_file, 'w', newline='') as output_csv:
    csv_reader = csv.DictReader(input_csv)
    fieldnames = ['movieId', 'img_url']
    csv_writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
    csv_writer.writeheader()

    for row in csv_reader:
        movie_id = row['movieId']
        tmdb_id = row['tmdbId']
        print(movie_id + " " + tmdb_id)
        # Send a request to TMDb to get movie details
        url = f'https://api.themoviedb.org/3/movie/{tmdb_id}?language=en-US'
        response = requests.get(url, headers={
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmYjk3MWVlZDQ4ODBlZDM0ZDIwMGRhMzVhOGE3Nzk0MiIsInN1YiI6IjY1MzNlMjY2YTBiZTI4MDExY2JiMTJjMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.R2Cv8H1kKd3flr508BP1ZPdogZNKzTvmLLf1ExOHQu4"
        })
        if response.status_code == 200:
            movie_data = response.json()
            # Extract the image URL
            image_url = f'{movie_data["poster_path"]}'

            # Write the data to the output CSV
            csv_writer.writerow({'movieId': movie_id, 'img_url': image_url})
        else:
            print(response)
            print(f'Failed to fetch details for movie with ID {movie_id}')

        print('Data extraction and writing to CSV completed.')