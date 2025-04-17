'''
Ryan Pascual, Yeehahn Wang-Liu
Intermediate Data Programming Period 1
Final Project
This file does the following types of work:
    * reduce the size of large datasets to something more manageable  
    * clean data: reduce/rename columns, normalize strings, adjust values  
    * generate data through relatively complicated calculations
'''
import pandas as pd
import ast


def preprocess_artists():
    '''
    Preprocesses artists.csv file by doing the following:
    - Removes artists with less than 100,000 followers
    - Removes artists with missing genre data
    - Removes 'id' column, which provides no value
    - Sorts artists by number of followers

    Returns preprocessed DataFrame from artists.csv
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

    return artists


def preprocess_artist_characteristics():
    '''
    Preprocesses spotify_dataset.csv by doing the following:
    - Filter dataset to relevant columns of musical characteristics
    - Aggregate single artist songs
    - Sort by popularity of artist
    - Drop duplicates

    Returns preprocessed DataFrame
    '''
    df = pd.read_csv('raw_data/spotify_dataset.csv')

    # All relevant columns for characteristics
    df = df[['valence', 'acousticness', 'artists', 'danceability', 'duration_ms', 'energy', 
             'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'popularity']]
    df = df.groupby('artists', as_index=False).mean()
    # Some songs have multiple artists but for clean data let's just agreggate single artist songs
    # This will make it easier when merging since the original artist dataset only has single artists
    df = df[df['artists'].apply(lambda x: ',' not in x)]
    # Reformat string to make more readable
    df['artists'] = df['artists'].apply(lambda x: x[2: -2])
    # Some artists have the same name so remove less popular duplicate
    df = df.sort_values(by='popularity')
    df = df.drop_duplicates('artists', keep='last')
    return df


def merge_artists():
    '''
    Preprocesses artists.csv and spotify_dataset.csv
    Merges both preprocessed datasets by artist
    Saves to .csv file titled 'artists.csv' in data_organized folder
    '''
    characteristics = preprocess_artist_characteristics()
    artists = preprocess_artists()

    characteristics = characteristics.loc[:, :'tempo']
    artists_merged = artists.merge(characteristics, left_on='artist', right_on='artists', how='inner')
    artists_merged.to_csv('data_organized/artists.csv', sep=',', index=False, encoding='utf-8')


def clean_spotify_dataset():
    '''
    The spotify_dataset is a very clean set of data
    Just need to clean up uncecesarry columns
    Saves the dataset to raw_data as spotify_dataset_clean and returns the df
    '''
    spotify_data = pd.read_csv('raw_data/spotify_dataset.csv')
    # Maintain only relevant columns
    spotify_data = spotify_data[['name', 'year', 'artists', 'valence', 'acousticness', 'danceability', 
                                 'duration_ms', 'energy', 'instrumentalness', 'liveness', 'loudness', 
                                 'popularity', 'speechiness', 'tempo']]

    spotify_data.to_csv('raw_data/spotify_dataset_clean.csv', sep=',', index=False, encoding='utf-8')
    return spotify_data


def create_final_spotify_dataset():
    '''
    Since the paper is looking for trends in popular music
    The spotify_dataset is filtered to just songs that are considered "popular"
    Saves the dataset to data_organized as spotify_dataset.csv
    '''
    spotify_data = clean_spotify_dataset()
    # Older songs need to be weighted more
    sufficiently_popular = (spotify_data['popularity'] - 0.4 * (spotify_data['year'] - 1920)) > 10

    spotify_data = spotify_data[sufficiently_popular]
    spotify_data.to_csv('data_organized/spotify_dataset.csv', sep=',', index=False, encoding='utf-8')


def clean_grammy():
    '''
    The grammy_award_dataset has a handful of unecesarry columns
    Removes those columns
    The artist column also has many missing artist names
    Fills in those names
    Saves the dataset to data_organized as grammy.csv
    '''
    grammy = pd.read_csv('raw_data/grammy_award_data.csv')
    # The year that the grammys are marked in this dataset are 1 year early
    grammy['year'] = grammy['year'] + 1
    grammy = grammy[['year', 'category', 'nominee', 'artist', 'workers']]

    songs = pd.read_csv('data_organized/spotify_dataset.csv', converters={'artists': ast.literal_eval})
    grammy = grammy.apply(lambda row: fill_artists(row, songs), axis=1)
    grammy.to_csv('data_organized/grammy.csv', sep=',', index=False, encoding='utf-8')


def fill_artists(grammy_row, songs):
    '''
    Fills in the missing artist names if 
    there is a corresponding song in the spotify_dataset
    Takes grammy_row (Pandas Series) and songs (Pandas DataFrame)
    Returns grammy_row with filled in artist column
    '''
    song_name = grammy_row['nominee']
    release_year = grammy_row['year']
    song_name_same = songs['name'] == song_name
    # Grammy selects from songs in a time frame that is within a year of the actual grammy
    similar_release = abs(songs['year'] - release_year) <= 1
    artist = songs['artists'][song_name_same & similar_release]

    if len(artist) > 0:
        grammy_row['artist'] = ', '.join(artist.iloc[0])

    return grammy_row


def grammy_songs_characteristics():
    '''
    Merges the spotify_dataset and the grammy dataset
    Now grammy song nominations have characteristics marked
    Saves the dataset to data_organized as grammy_song_characteristics.csv
    '''
    grammy = pd.read_csv('data_organized/grammy.csv')
    grammy = grammy[['year', 'category', 'nominee', 'workers']]
    spotify_dataset = pd.read_csv('data_organized/spotify_dataset.csv')
    spotify_dataset = spotify_dataset.rename(columns={'name': 'spotify_name', 'year': 'spotify_year'})

    grammy_song = grammy.merge(spotify_dataset, left_on=['nominee', 'year'], 
                               right_on=['spotify_name', 'spotify_year'], how='inner')
    # These columns are just repeat of other the name and year column
    grammy_song = grammy_song.drop(['spotify_name', 'spotify_year'], axis=1)
    grammy_song.to_csv('data_organized/grammy_song_char.csv', sep=',', index=False, encoding='utf-8')


def clean_genres():
    '''
    Removes unecesarry columns in data_by_genres.csv
    Otherwise the genres dataset is clean
    Saves the dataset to data_organized as genres.csv
    '''
    genres = pd.read_csv('raw_data/data_by_genres.csv')
    genres = genres.drop(['mode', 'key'], axis=1)
    genres.to_csv('data_organized/genres.csv', sep=',', index=False, encoding='utf-8')


def main():
    merge_artists()
    create_final_spotify_dataset()
    clean_grammy()
    grammy_songs_characteristics()
    clean_genres()


if __name__ == '__main__':
    main()