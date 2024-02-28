import advertools as adv
import pandas as pd
from urllib.parse import urlparse, unquote
import re
import os

def extract_cured_name(url):
    path = urlparse(unquote(url)).path
    path = path.strip('/')
    name = path.split('/')[-1]
    name = re.sub(r'\.\w+$', '', name).split('?')[0]
    name = name.replace('-', ' ').replace('_', ' ').strip()
    if name.replace(' ', '').isdigit() or not name:
        return ''
    return name

sitemap_urls = [
    'https://www.kevinrchant.com/post-sitemap.xml',
    'https://thomas-leblanc.com/sitemap-1.xml',
    'https://www.oliviertravers.com/post-sitemap.xml',
    'https://data-mozart.com/post-sitemap.xml',
    'https://www.sqlbi.com/wp-sitemap-posts-post-1.xml',
    'https://en.brunner.bi/blog-posts-sitemap.xml',
    'https://pragmaticworks.com/sitemap.xml',
    'https://data-marc.com/sitemap.xml',
    'https://www.data-traveling.com/sitemap.xml',
    'https://datasavvy.me/sitemap.xml',
    'https://www.thatbluecloud.com/sitemap-posts.xml',
]

all_sitemaps_df = pd.DataFrame()

for sitemap_url in sitemap_urls:
    website = urlparse(sitemap_url).netloc
    sitemap = adv.sitemap_to_df(sitemap_url)
    sitemap['lastmod'] = pd.to_datetime(sitemap['lastmod']).dt.strftime('%Y-%m-%d')
    sitemap['cured_name'] = sitemap['loc'].apply(extract_cured_name)
    filtered_sitemap = pd.DataFrame({
        'website': website,
        'loc': sitemap['loc'],
        'lastmod': sitemap['lastmod'],
        'cured_name': sitemap['cured_name']
    })
    all_sitemaps_df = pd.concat([all_sitemaps_df, filtered_sitemap], ignore_index=True)

# Save to the data directory
script_directory = os.path.dirname(os.path.abspath(__file__))
data_directory = os.path.join(script_directory, 'data')
os.makedirs(data_directory, exist_ok=True)  # Create 'data' directory if it does not exist
all_sitemaps_df.to_csv(os.path.join(data_directory, 'article_blog.csv'), index=False)

print(all_sitemaps_df.head())
