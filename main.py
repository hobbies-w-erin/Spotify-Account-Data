import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime

# Load data from a JSON file
with open('StreamingHistory_music_0.json', 'r') as file:
    data = json.load(file)

# Create DataFrame from JSON data
df = pd.DataFrame(data)

# Convert 'endTime' to datetime object and extract date, month
df['endTime'] = pd.to_datetime(df['endTime'])
df['date'] = df['endTime'].dt.date
df['month'] = df['endTime'].dt.to_period('M')  # Extract month

# Task 1: Top 12 songs per month based on total time played
top_songs_per_month = df.groupby(['month', 'trackName']).agg({'msPlayed': 'sum'}).reset_index()
top_songs_per_month['hoursPlayed'] = top_songs_per_month['msPlayed'] / (1000 * 60 * 60)  # Convert ms to hours

# Get top 12 songs by playtime per month
top_12_songs = top_songs_per_month.groupby('month').apply(lambda x: x.nlargest(12, 'msPlayed')).reset_index(drop=True)

# Visualize the top 12 songs for each month
for month, group in top_12_songs.groupby('month'):
    plt.figure(figsize=(10, 6))
    plt.barh(group['trackName'], group['hoursPlayed'], color='skyblue')
    plt.title(f'Top 12 Songs in {month}')
    plt.xlabel('Hours Played')
    plt.ylabel('Song Name')
    plt.gca().invert_yaxis()
    plt.show()

# Task 2: Song played the most each day
most_played_per_day = df.groupby(['date', 'trackName']).agg({'msPlayed': 'sum'}).reset_index()
most_played_per_day = most_played_per_day.loc[most_played_per_day.groupby('date')['msPlayed'].idxmax()]

# Display the song played the most each day
print("Song played the most each day:")
print(most_played_per_day[['date', 'trackName', 'msPlayed']])