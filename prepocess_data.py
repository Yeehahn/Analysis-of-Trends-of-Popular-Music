import pandas as pd
'''
This file is intended to do the following types of work:
    * download data from APIs  
    * screenscrape data from websites  
    * reduce the size of large datasets to something more manageable  
    * clean data: reduce/rename columns, normalize strings, adjust values  
    * generate data through relatively complicated calculations   
'''


def clean_artists():
    '''
    Decreases the amount of entries in the artists.csv
    artists.csv is filled with artists who have very little followers and/or no associated genres
    These artists give us little value to our research questions so should be removed.
    '''
    artists = pd.read_csv('raw_data/artists.csv')
    follower_filter = artists['followers'] > 100000
    genres_filter = artists['genres'].apply(len) > 2
    artists = artists[follower_filter & genres_filter]
    # The id column is useless for us
    artists = artists[['followers', 'genres', 'artist', 'popularity']]
    # There are some artists with the same name
    # We will remove the artist that is less popular for cleanliness of data
    # There are only 12 artists like this so the change in data is minimal
    artists = artists.sort_values(by='popularity')
    artists = artists.drop_duplicates('artist', keep='last')

    artists.to_csv('data_organized/artists.csv', sep=',', index=False, encoding='utf-8')


def find_artist_characteristics():
    '''
    artists.csv does not tell us the characteristics of the artists music
    so we need to find the artists characteristics using spotify_dataset and merge
    all relveant columns to create a robust dataset
    '''
    df = pd.read_csv('raw_data/spotify_dataset.csv')

    # All relevant columns for characteristics
    df = df[['valence', 'acousticness', 'artists', 'danceability', 'duration_ms', 'energy', 
             'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'popularity']]
    df = df.groupby('artists', as_index=False).mean()
    # Some songs have multiple artists but for clean data let's just agreggate single artist songs
    # This will make it easier when merging 
    df = df[df['artists'].apply(lambda x: ',' not in x)]
    df['artists'] = df['artists'].apply(lambda x: x[2: -2])
    # Some artists have the same name so remove less popular artist for clean data
    df = df.sort_values(by='popularity')
    df = df.drop_duplicates('artists', keep='last')
    df.to_csv('data_organized/artists_char.csv', sep=',', index=False, encoding='utf-8')


def merge_artists():
    '''
    There is artists_char and artists
    artists has genres and follower count
    artists_char has the artist music characteristics
    Merging them will create a complete dataset for artists
    '''
    characteristics = pd.read_csv('data_organized/artists_char.csv')
    artists = pd.read_csv('data_organized/artists.csv')

    characteristics = characteristics.loc[:, :'tempo']
    artists_merged = artists.merge(characteristics, left_on='artist', right_on='artists', how='inner')
    print(artists_merged.head())


find_artist_characteristics()