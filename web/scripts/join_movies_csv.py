import pandas as pd

# Assuming you have three CSV files: csv_file1.csv, csv_file2.csv, and csv_file3.csv
df1 = pd.read_csv('web_movie.csv')
df2 = pd.read_csv('movie_without_tag.csv')
df3 = pd.read_csv('movie.csv')
print(df3)
# Specify the common column on which you want to join the DataFrames
common_column = 'movie_id'

df3.append(df2)
df2 = df3
print(df2)

df2.to_csv('C:\\Users\\maria\\PycharmProjects\\movie_rec\\web\\scripts\\merged.csv', index=False)

selected_columns = ['movie_id','rating_mean','rating_median','num_ratings','movie_tags','comparable']
df2 = df2[selected_columns]

print(df2)
# Merge the DataFrames
merged_df = pd.merge(df1, df2, on=common_column, how='inner')

print(merged_df)

# Now, merged_df contains the result of the join
merged_df.to_csv('C:\\Users\\maria\\PycharmProjects\\movie_rec\\web\\scripts\\output.csv', index=False)
