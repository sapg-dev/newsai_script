import pandas as pd
import os

# Define the base path using the script's directory
script_directory = os.path.dirname(os.path.abspath(__file__))
data_directory = os.path.join(script_directory, 'data')

# Paths to the source CSV files
article_blog_csv_path = os.path.join(data_directory, 'article_blog.csv')
youtube_videos_csv_path = os.path.join(data_directory, 'youtube_videos.csv')

# Read the article blog CSV file and add a 'type' column
df_article_blog = pd.read_csv(article_blog_csv_path)
df_article_blog['type'] = 'blog'  # Add 'type' column for blog articles

# Read the YouTube videos CSV file and add a 'type' column
df_youtube_videos = pd.read_csv(youtube_videos_csv_path)
df_youtube_videos['type'] = 'youtube'  # Add 'type' column for YouTube videos

# Concatenate the two DataFrames
df_sitemap = pd.concat([df_article_blog, df_youtube_videos], ignore_index=True)

# Save the concatenated DataFrame to a new CSV file
sitemap_csv_path = os.path.join(data_directory, 'sitemap.csv')
df_sitemap.to_csv(sitemap_csv_path, index=False)

print(f'Sitemap CSV has been created at: {sitemap_csv_path}')
