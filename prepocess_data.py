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
import re


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
    artists_merged = multiply_characteristics_100(artists_merged)
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
    spotify_data['decade'] = spotify_data['year'].floordiv(10).mul(10)
    spotify_data['duration_s'] = spotify_data['duration_ms'] / 1000
    spotify_data.to_csv('raw_data/spotify_dataset_clean.csv', sep=',', index=False, encoding='utf-8')
    return spotify_data


def create_final_spotify_dataset():
    '''
    Since the paper is looking for trends in popular music
    The spotify_dataset is filtered to just songs that are considered "popular"
    Creates a second dataset of all of the unpopular music
    Saves the dataset to data_organized as spotify_dataset.csv and unpopular_music.csv
    '''
    spotify_data = clean_spotify_dataset()
    # Older songs need to be weighted more
    sufficiently_popular = (spotify_data['popularity'] - 0.4 * (spotify_data['year'] - 1920)) > 10
    sufficiently_unpopular = (spotify_data['popularity'] - 0.4 * (spotify_data['year'] - 1920)) <= 10
    spotify_data_popular = spotify_data[sufficiently_popular]
    unpopular = spotify_data[sufficiently_unpopular]

    spotify_data_popular = multiply_characteristics_100(spotify_data)
    unpopular = multiply_characteristics_100(unpopular)
    spotify_data_popular.to_csv('data_organized/spotify_dataset.csv', sep=',', index=False, encoding='utf-8')
    unpopular.to_csv('data_organized/unpopular_music.csv', sep=',', index=False, encoding='utf-8')


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
    grammy = grammy[['year', 'category', 'artist', 'workers', 'nominee', 'winner']]

    songs = pd.read_csv('data_organized/spotify_dataset.csv', converters={'artists': ast.literal_eval})
    songs['name'] = songs['name'].str.lower()
    songs_dict = dict_songs(songs)
    grammy = grammy.apply(lambda row: fill_artists(row, songs_dict), axis=1)
    grammy['artist'] = grammy['artist'].apply(clean_artist_col)
    grammy.to_csv('data_organized/grammy_award_data.csv', sep=',', index=False, encoding='utf-8')


def dict_songs(songs):
    song_dict = dict()

    for index, row in songs.iterrows():
        name = row['name']
        year = row['year']
        artists = row['artists']
        if (name, year) in song_dict.keys():
            song_dict[(name, year)].extend(artists)
        else:
            song_dict[(name, year)] = artists

    return song_dict


def clean_artist_col(artist):
    '''
    The artist column in grammy_award_data is very inconsistent in how it presents the artists
    It strings multiple artists together with a comma, and, or &. It also includes role jobs
    such as engineer, conductor, songwriters.
    All of these are irrelevant and this method turns that convoluted string into a list of relevant artists
    '''
    # Re-creating this set everytime is slow however the dataset is small enough where
    # This does not have significant effects on performacne and makes it easier to read
    # This does NOT fully filter out all role words
    # It filters out the most common such that the remaining have no influence on the results
    # of our analysis
    if pd.notna(artist):
        role_words = {'engineer', 'conductor', 'songwriters', 'composer', 'vocals', 'arranger', 
                      'various artists', 'artists', 'soloist', 'producer', 'songwriter', 'art director',
                      'note writer', 'artist', 'album notes writer', 'art directors', 'engineers', 'engineer',
                      'mastering engineer', 'producers', 'composers', 'arrangers', 'remixer', 'soloists', 
                      'mastering engineers', 'ensembles', 'ensemble'}
        # Filters for everything outside of parentheses
        # Typically everything inside parentheses is unecesarry
        out_paren = re.sub(r'\([^)]*\)', '', artist)
        # Filters for the comma, and, &, and featuring and ignroes case
        # The actual filter for delimiters was partially filled in by ChatGPT
        raw_names = re.split(r'(?i)\s*[&,]\s*|\s+and\s+|\s+featuring\s+', out_paren)

        cleaned = set()
        for name in raw_names:
            name = name.strip()
            if name and name.lower() not in role_words:
                cleaned.add(name)
        return list(cleaned)


def fill_artists(grammy_row, songs_dict):
    '''
    Fills in the missing artist names if 
    there is a corresponding song in the spotify_dataset
    Takes grammy_row (Pandas Series) and songs (Pandas DataFrame)
    Returns grammy_row with filled in artist column
    '''
    # Sometimes the name is a series of numbers
    song_name = str(grammy_row['nominee']).lower()
    release_year = grammy_row['year']
    # Make it case insensitive
    # Grammy selects from songs in a time frame that is within a year of the actual grammy
    # Make it two just to be sure the song is grabbed
    artists = []
    for year_offset in range(-1, 1):
        year = release_year + year_offset
        if (song_name, year) in songs_dict:
            artists.append(songs_dict[(song_name, year)])

    if len(artists) > 0:
        grammy_row['artist'] = '& '.join(artists[0])

    return grammy_row


def grammy_songs_characteristics():
    '''
    Merges the spotify_dataset and the grammy dataset
    Now grammy song nominations have characteristics marked
    Saves the dataset to data_organized as grammy_song_characteristics.csv
    '''
    grammy = pd.read_csv('data_organized/grammy_award_data.csv', converters={'artist': list_eval})
    grammy = grammy[['category', 'nominee', 'artist', 'workers']]
    no_records_albums = grammy['category'].apply(lambda x: 'Album' not in x and 
                                                 'Record' not in x)
    grammy = grammy[no_records_albums]
    # Songs should be released 1 year before from the actual Grammy awards
    spotify_dataset = pd.read_csv('data_organized/spotify_dataset.csv', 
                                  converters={'artists': ast.literal_eval})
    # Normalizing names
    grammy['nominee_clean'] = grammy['nominee'].str.lower().str.strip()
    grammy['artist_clean'] = grammy['artist'].apply(sorted).apply(str)
    spotify_dataset['spotify_name_clean'] = spotify_dataset['name'].str.lower().str.strip()
    spotify_dataset['spotify_artist_clean'] = spotify_dataset['artists'].apply(sorted).apply(str)

    grammy_song = grammy.merge(spotify_dataset, left_on=['nominee_clean', 'artist_clean'], 
                               right_on=['spotify_name_clean', 'spotify_artist_clean'], how='inner')
    # These columns are just repeat of other the name and year column
    grammy_song = grammy_song.drop(['spotify_name_clean', 'spotify_artist_clean', 'artists',
                                    'artist_clean', 'nominee_clean'], 
                                   axis=1)
    grammy_song.to_csv('data_organized/grammy_song_char.csv', sep=',', index=False, encoding='utf-8')


def list_eval(artist_list):
    if pd.isna(artist_list) or artist_list == '':
        return []
    else:
        return ast.literal_eval(artist_list)


def clean_genres():
    '''
    Removes unecesarry columns in data_by_genres.csv
    Otherwise the genres dataset is clean
    Saves the dataset to data_organized as genres.csv
    '''
    genres = pd.read_csv('raw_data/data_by_genres.csv')
    genres = genres.drop(['mode', 'key'], axis=1)
    genres = multiply_characteristics_100(genres)
    genres.to_csv('data_organized/data_by_genres.csv', sep=',', index=False, encoding='utf-8')


def multiply_characteristics_100(df):
    '''
    Visually a scale from 0.0 to 1.0 is not as appealing as a scale from 0 to 100
    Scales all of the values that go from 0.0 to 1.0 to go from 0 to 100
    '''
    characteristics = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness',
                       'speechiness', 'valence']
    df[characteristics] = df[characteristics] * 100
    return df


def main():
    merge_artists()
    create_final_spotify_dataset()
    clean_grammy()
    grammy_songs_characteristics()
    clean_genres()
    print('done')


if __name__ == '__main__':
    main()