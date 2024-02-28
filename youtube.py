import requests
import csv
from datetime import datetime
import os

api_key = "AIzaSyCVu4izhQztNO_9IDGXDuivhgaE-WP_8t0"  # Replace with your actual API key
channels = {
    "UCFp1vaKzpfvoGai0vE5VJ0w": "GuyInACube",
    "UCcfngi7_ASuo5jdWX0bNauQ": "HowToPowerBI",
}

def fetch_videos(channel_id, channel_name):
    base_url = "https://www.googleapis.com/youtube/v3/search"
    videos = []
    page_token = ""
    
    while True:
        params = {
            'part': 'snippet',
            'channelId': channel_id,
            'maxResults': 5,
            'order': 'date',
            'type': 'video',
            'key': api_key,
            'pageToken': page_token,
            'publishedAfter': '2021-01-01T00:00:00Z'
        }
        
        response = requests.get(base_url, params=params).json()
        items = response.get('items', [])
        
        for item in items:
            video_id = item['id'].get('videoId', '')
            title = item['snippet'].get('title', '')
            publish_date = datetime.strptime(item['snippet'].get('publishedAt', '1900-01-01T00:00:00Z'), '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append((channel_name, video_url, publish_date, title))
        
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    
    return videos

# Saving part
script_directory = os.path.dirname(os.path.abspath(__file__))
data_directory = os.path.join(script_directory, 'data')
os.makedirs(data_directory, exist_ok=True)
csv_file_path = os.path.join(data_directory, 'youtube_videos.csv')

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["website", "loc", "lastmod", "cured_name"])
    for channel_id, channel_name in channels.items():
        videos = fetch_videos(channel_id, channel_name)
        for video in videos:
            writer.writerow(video)

print("CSV file has been created with the updated videos information.")
