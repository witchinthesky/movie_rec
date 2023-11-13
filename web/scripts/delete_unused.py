import pandas as pd

# Assuming you have three CSV files: csv_file1.csv, csv_file2.csv, and csv_file3.csv
out = pd.read_csv('output.csv')
df2 = pd.read_csv('web_link.csv')
df3 = pd.read_csv('web_tag.csv')
df4 = pd.read_csv('web_rating.csv')

# Specify the common column on which you want to join the DataFrames
common_column = 'movie_id'

merged_df = pd.merge(out, df2, on=common_column, how='left')

selected_columns = ['movie_id','rating_mean','rating_median','num_ratings','movie_tags','comparable']
df2 = df2[selected_columns]
# Merge the DataFrames


print(merged_df)

# Now, merged_df contains the result of the join
merged_df.to_csv('C:\\Users\\maria\\PycharmProjects\\movie_rec\\web\\scripts\\output.csv', index=False)
