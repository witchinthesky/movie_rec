import csv
import pandas as pd
from faker import Faker
import random
import string

# Set up Faker for generating random names
fake = Faker()

# Read the ratings.csv file
ratings_df = pd.read_csv("C:\\Users\\maria\\PycharmProjects\\movie_rec\\web\\scripts\\rating.csv")

# Get unique user IDs from the ratings dataframe
unique_user_ids = ratings_df['userId'].unique()

# Generate a random username and password for each unique user ID
user_credentials = []
generated_usernames = set()

def generate_unique_username():
    while True:
        username = fake.user_name()
        if username not in generated_usernames:
            generated_usernames.add(username)
            return username

for user_id in unique_user_ids:
    username = generate_unique_username()
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    email = fake.email()
    user_credentials.append({'id': user_id,
                             'password': password,
                             'last_login': "2023-11-11 14:36:17.875821",
                             'is_superuser': 0,
                             'username': username,
                             'last_name': username,
                             'email': email,
                             'is_staff': 0,
                             'is_active': 1,
                             'date_joined': "2023-10-21 17:40:57.194032",
                             'first_name': username})

    # Log information for each user
    print(f"Generated credentials for user ID {user_id}: Username - {username}, Password - {password}")

# Create a dataframe from the list of user credentials
users_df = pd.DataFrame(user_credentials)

output_file = "C:\\Users\\maria\\PycharmProjects\\movie_rec\\web\\scripts\\users_with_credentials.csv"

with open(output_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(users_df.columns)  # Write header
    csv_writer.writerows(users_df.values)

# Log the completion of the process
print("User credentials generation completed.")
