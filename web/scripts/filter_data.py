import csv
import re

input2_csv_file = "C:\\Users\\maria\\PycharmProjects\\movie_rec\\web\\output.csv"
input_csv_file = "C:\\Users\\maria\\PycharmProjects\\movie_rec\\web\\movie.csv"
input3_csv_file = "C:\\Users\\maria\\PycharmProjects\\movie_rec\\web\\link.csv"
output_csv_file = "C:\\Users\\maria\\PycharmProjects\\movie_rec\\web\\output2.csv"

with open(input_csv_file, 'r') as input_csv, open(input2_csv_file, 'r') as input2_csv, open(input3_csv_file, 'r') as input3_csv, open(output_csv_file, 'w', newline='') as output_csv:
    csv_reader = csv.DictReader(input_csv)
    csv_reader2 = csv.DictReader(input2_csv)
    csv_reader3 = csv.DictReader(input3_csv)
    fieldnames = ['id', 'title', 'release_year', 'img_url', 'genres', 'tmdb_id']
    csv_writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
    csv_writer.writeheader()

    for row in csv_reader:
        poster_url = ""
        tmdb_id = ""

        input2_csv.seek(0)  # Reset the input2_csv to the beginning
        input3_csv.seek(0)  # Reset the input3_csv to the beginning

        for r in csv_reader2:
            if row['movieId'] == r['movieId']:
                poster_url = r['img_url']
                print(row['movieId'] + poster_url)
                break

        for r in csv_reader3:
            if row['movieId'] == r['movieId']:
                tmdb_id = r['tmdbId']
                break

        title = row['title']
        match = re.search(r'^(.*?)\s*\((\d{4})\)', title)
        if match:
            title = match.group(1).strip()
            year = match.group(2)
        else:
            print("No match found.")

        if poster_url != 'None' and poster_url != "":
            csv_writer.writerow({'id': row['movieId'], 'title': title, 'release_year': year,
                                 'img_url': poster_url, 'genres': row['genres'], 'tmdb_id': tmdb_id})
