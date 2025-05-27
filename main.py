'''
Create amazing plots in this file. You will read the data from `data_organized` 
(unless your raw data required no reduction, in which case you can read your data from `raw_data`). 
You will do plot-related work such as joins, column filtering, pivots, 
small calculations and other simple organizational work. 
'''
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import re


def create_characteristic_vs_time():
    '''
    Plots the Change the Time vs Characteristic linear regression graph 
    outlined in the README.MD in plots
    Plot is created in Q_1/characteristic_vs_time_Q1
    It is called Change in Danceability Over Time in the README however this method creates
    a graph for all numerical characteristics given by spotify
    '''
    sns.set()
    spot_df = pd.read_csv('data_organized/spotify_dataset.csv')
    spot_df = spot_df.drop(['name', 'artists'], axis=1)
    spot_df = spot_df.groupby('year').mean()

    characteristic_100_range = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                                'liveness', 'speechiness', 'valence']
    characteristic_not_100_range = ['duration_ms', 'loudness', 'tempo']

    for characteristic in characteristic_100_range:
        sns.regplot(x=spot_df.index, y=characteristic, data=spot_df)
        plt.ylim((0, 100))
        adjust_plot_characteristic(characteristic, 'plots/Q_1/characteristic_vs_time_Q1/',
                                   '_vs_time_reg')

    for characteristic in characteristic_not_100_range:
        sns.regplot(x=spot_df.index, y=characteristic, data=spot_df)
        adjust_plot_characteristic(characteristic, 'plots/Q_1/characteristic_vs_time_Q1/',
                                   '_vs_time_reg')
    plt.clf()


def create_box_characteristic_vs_time():
    '''
    Plots the Change the Time vs Characteristic box plot graph 
    outlined in the README.MD in plots
    Plot is created in Q_1/characteristic_vs_time_Q1
    It is called Change in Danceability Over Time in the README however this method creates
    a graph for all numerical characteristics given by spotify
    '''
    sns.set()
    spot_df = load_spot_df_for_char()
    characteristic_100_range = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                                'liveness', 'speechiness', 'valence']
    characteristic_not_100_range = ['duration_ms', 'loudness', 'tempo']

    for characteristic in characteristic_100_range:
        sns.boxplot(x='decade', y=characteristic, data=spot_df, showfliers=False)
        plt.ylim((0, 100))
        adjust_plot_characteristic(characteristic, 'plots/Q_1/characteristic_vs_time_Q1/',
                                   '_vs_time_box')

    for characteristic in characteristic_not_100_range:
        sns.boxplot(x='decade', y=characteristic, data=spot_df, showfliers=False)
        adjust_plot_characteristic(characteristic, 'plots/Q_1/characteristic_vs_time_Q1/',
                                   '_vs_time_box')
    plt.clf()


def adjust_plot_characteristic(characteristic, folder_path, title):
    '''
    Used in the characteristic_vs_time graphs
    Sets the xlabel, ylabel, title, and saves the plot to the correct location 
    with the correct name
    '''
    capital_characteristic = characteristic.capitalize()
    plt.title('Change in ' + capital_characteristic + ' Over Time')
    plt.xlabel('Year')
    plt.ylabel(capital_characteristic)
    file_name = characteristic + title
    plt.savefig(folder_path + file_name, bbox_inches='tight')
    plt.clf()


def plot_all_characteristic_of_music():
    sns.set()
    spot_df = pd.read_csv('data_organized/spotify_dataset.csv')
    spot_df = spot_df[['acousticness', 'danceability', 'energy', 'instrumentalness',
                       'liveness', 'speechiness', 'valence', 'year']]
    char_col = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                       'liveness', 'speechiness', 'valence']
    for char in char_col:
        # Smoothing the values so the graph is easier to read
        spot_df[char] = spot_df[char].rolling(window=5).mean()

    characteristics = spot_df.groupby('year').mean()
    characteristics.plot()
    plt.legend(['Acousticness', 'Danceability', 'Energy', 'Instrumentalness',
                'Liveness', 'Speechiness', 'Valence'], loc='upper right', fontsize='x-small')
    plt.ylim(0, 100)
    plt.xlabel('Year')
    plt.ylabel('Characteristic Value')
    plt.title('All Characteristics of Music Over Time')
    plt.savefig('plots/Q_1/all_char_over_time', bbox_inches='tight')
    plt.clf()


def plot_characteristic_histogram():
    '''
    Creates the histograms of each characteristic for each decade from 1990-2010
    Plot is created in plots/Q_2
    Characteristics in Popular Music is the name in the README
    '''
    sns.set()
    spot_df = load_spot_df_for_char()
    spot_df = spot_df[(spot_df['decade'] >= 1990) & (spot_df['decade'] < 2020)]
    characteristic_100_range = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                                'liveness', 'speechiness', 'valence']
    decade_char = spot_df.groupby('decade')[characteristic_100_range].mean()

    x_axis = np.arange(3)
    bar_width = 0.1
    fig, ax = plt.subplots(figsize=(14, 6))


    # Since this plot plots the x-axis as decades but it needs to be separated by characteristics
    # Have to manually place bars onto the plot and then set them with a legend
    for i, char in enumerate(characteristic_100_range):
        ax.bar(x_axis + i * bar_width, decade_char[char], bar_width, label=char)

    # X-axis labels
    # Have to manually set the labels to be decades instead of the characteristics
    ax.set_xticks(x_axis + bar_width * len(characteristic_100_range) / 2)
    ax.set_xticklabels([1990, 2000, 2010])

    plt.ylabel('Average Value of Characteristic')
    plt.title('Characteristics of Popular Music by Decade')
    plt.legend()
    plt.savefig('plots/Q_2/characteristic_histogram', bbox_inches='tight')
    plt.clf()


def plot_difference_characteristic_histogram():
    '''
    Creates the histogram that subtracts the average value of popular music - unpopular music
    from 1990-2010
    Plot is created in plots/Q_2
    Differences in Characteristics of Popular Music and Unpopular Music in README
    Reference README to see more detailed description and reasoning behind plot
    '''
    spot_df = load_spot_df_for_char()
    spot_df = spot_df[(spot_df['decade'] >= 1990) & (spot_df['decade'] < 2020)]
    characteristic_100_range = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                                'liveness', 'speechiness', 'valence']
    
    unpop_df = pd.read_csv('data_organized/unpopular_music.csv')
    unpop_df = unpop_df.drop(['name', 'artists'], axis=1)
    unpop_df['decade'] = unpop_df['year'].floordiv(10).mul(10)
    unpop_df = unpop_df[(unpop_df['decade'] >= 1990) & (unpop_df['decade'] < 2020)]

    decade_pop_char = spot_df.groupby('decade')[characteristic_100_range].mean()
    decade_unpop_char = unpop_df.groupby('decade')[characteristic_100_range].mean()
    decade_char = decade_pop_char - decade_unpop_char

    x_axis = np.arange(3)
    bar_width = 0.1
    fig, ax = plt.subplots(figsize=(14, 6))

    for i, char in enumerate(characteristic_100_range):
        ax.bar(x_axis + i * bar_width, decade_char[char], bar_width, label=char)

    # X-axis labels
    # Have to manually set the labels to be decades instead of the characteristics
    ax.set_xticks(x_axis + bar_width * len(characteristic_100_range) / 2)
    ax.set_xticklabels([1990, 2000, 2010])

    plt.ylabel('Average Difference Value of Characteristic')
    plt.title('Characteristics of Popular - Unpopular Music by Decade')
    plt.ylim(-50, 50)
    plt.legend()
    plt.savefig('plots/Q_2/characteristic_difference_histogram', bbox_inches='tight')
    plt.clf()


def load_spot_df_for_char():
    '''
    The spotify_dataset is a good dataset and all of the columns are often used
    However, when looking at average characterisitcs strings cause issues with aggregate functions
    Loads in the spotify dataset with some more pre-processing (drops name and artist columns)
    '''
    spot_df = pd.read_csv('data_organized/spotify_dataset.csv')
    spot_df = spot_df.drop(['name', 'artists'], axis=1)
    return spot_df


def char_violin_plot():
    '''
    Plots a violin plot for all numeric characteristics ranging from 0 - 100
    Each decade from 1920-2020 gets its own plot
    Plot is created in plots/Q_2/decade_violin_plot
    Violin Plot of Characteristics of Popular Music in README
    Reference for further description
    '''
    spot_df = load_spot_df_for_char()
    relevant_columns = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                        'liveness', 'speechiness', 'valence', 'decade']
    spot_df = spot_df[relevant_columns]

    for decade in range(1920, 2021, 10):
        decade_data = spot_df[spot_df['decade'] == decade].drop('decade', axis=1)
        plt.violinplot(decade_data, showmeans=True, showextrema=False)
        plt.xticks(ticks=[1, 2, 3, 4, 5, 6, 7], 
                   labels=['Acou', 'Dance', 'Energy', 'Instru',
                           'Live', 'Speech', 'Val'])
        plt.ylim(0, 100)
        plt.title(str(decade) + '\'s Characteristic Violin Plot')
        plt.ylabel('Average Values')
        plt.xlabel('Characteristics')
        plt.savefig('plots/Q_2/decade_violin_plot/' + str(decade))
        plt.clf()


def smoothed_char_vs_pop():
    spot_df = load_spot_df_for_char()
    relevant_columns = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                        'liveness', 'speechiness', 'valence', 'popularity']
    spot_df = spot_df[relevant_columns]
    spot_df = spot_df.groupby('popularity').mean()

    for char in spot_df:
        spot_df[char] = spot_df[char].rolling(window=5).mean()

    plt.plot(spot_df)
    plt.ylim(0, 100)
    plt.legend(['Acousticness', 'Danceability', 'Energy', 'Instrumentalness',
                'Liveness', 'Speechiness', 'Valence'], loc='upper right', fontsize='x-small')
    plt.title('Popularity Vs. Characteristic Value')
    plt.ylabel('Average Values')
    plt.xlabel('Popualrity')
    plt.savefig('plots/Q_2/Smoothed_Popularity_vs_characteristic')
    plt.clf()


def plot_char_vs_pop():
    '''
    '''
    spot_df = load_spot_df_for_char()
    relevant_columns = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                        'liveness', 'speechiness', 'valence', 'popularity']
    spot_df = spot_df[relevant_columns]
    spot_df = spot_df.groupby('popularity').mean()

    plt.plot(spot_df)
    plt.ylim(0, 100)
    plt.legend(['Acousticness', 'Danceability', 'Energy', 'Instrumentalness',
                'Liveness', 'Speechiness', 'Valence'], loc='upper right', fontsize='x-small')
    plt.title('Popularity Vs. Characteristic Value')
    plt.ylabel('Average Values')
    plt.xlabel('Popualrity')
    plt.savefig('plots/Q_2/Popularity_vs_characteristic')
    plt.clf()


def r_value_char_bar():
    spot_df = load_spot_df_for_char()
    relevant_columns = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                        'liveness', 'speechiness', 'valence', 'popularity']
    spot_df = spot_df[relevant_columns]
    spot_df = spot_df.groupby('popularity').mean().reset_index()
    correlations = spot_df.corr(method='pearson')
    r_sq_values = pd.DataFrame({'characteristic': [], 
                                'value': []})
    relevant_columns.remove('popularity')

    for i, char in enumerate(relevant_columns):
        r_val = correlations.loc['popularity', char]
        r_sq_values.loc[i] = {'characteristic': char.capitalize(), 'value': r_val}

    sns.barplot(r_sq_values, x='characteristic', y='value')
    plt.xlabel('Characteristics')
    plt.xticks(rotation=30)
    plt.ylabel('r Values')
    plt.title('r values of Popularity vs. Characteristics')
    plt.savefig('plots/Q_2/r_popularity_vs_characteristics', bbox_inches='tight')
    plt.clf()


def grammy_characteristic_violin_plot():
    '''
    Plots a violin plot comparing each characteristic (acousticness, danceability,
    instrumentalness, valence, liveness, speechiness) for Grammy winners and for 
    general popular music
    '''
    relevant_columns = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                    'liveness', 'speechiness', 'valence']
    df_grammy = pd.read_csv('data_organized/grammy_song_char.csv')
    df_pop = pd.read_csv('data_organized/spotify_dataset.csv')

    # Normalize columns
    df_grammy[relevant_columns] = df_grammy[relevant_columns] / 10000
    df_pop[relevant_columns] = df_pop[relevant_columns] / 100

    df_grammy = df_grammy.drop_duplicates(subset=['name', 'artists'])
    df_grammy['label'] = 'Grammy Winners'
    df_pop['label'] = 'Popular Music'

    necessary_columns = ['name', 'artists'] + relevant_columns + ['label']
    df = pd.concat([df_grammy[necessary_columns], df_pop[necessary_columns]])
    melted_df = pd.melt(df, id_vars='label', value_vars=relevant_columns,
                        var_name='Characteristic', value_name='Value')

    sns.violinplot(x='Characteristic', y='Value', hue='label',
                   data=melted_df, inner='quartile')
    plt.title('Characteristics of Grammy Nominees vs. Popular Music')
    plt.xlabel('Characteristic')
    plt.ylabel('Value')
    plt.legend(title='label')
    plt.xticks(rotation=45)
    plt.savefig('plots/Q_3/grammy_characteristic_violin_plot', bbox_inches='tight')
    plt.clf()


def percent_grammy_nominees_with_characteristic_plot():
    '''
    Plots a bar chart that displays each relevant characteristic (acousticness, danceability,
    instrumentalness, valence, liveness, speechiness) and what percentage of Grammy winners
    have a score of above 70 (a reasonably high score) for that characteristic
    '''
    df = pd.read_csv('data_organized/grammy_song_char.csv')
    relevant_columns = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                    'liveness', 'speechiness', 'valence']
    df[relevant_columns] = df[relevant_columns] / 10000
    df = df.drop_duplicates(subset=['name', 'artists'])
    threshold = 0.64
    # Calculate percentage of songs above threshold for each characteristic
    high_scores = {
        col: (df[col] > threshold).mean() * 100
        for col in relevant_columns
    }

    df_scores = pd.DataFrame({'Characteristic': list(high_scores.keys()),
                              'Percentage': list(high_scores.values())})
    
    sns.barplot(x='Characteristic', y='Percentage', data=df_scores)
    plt.title('Percentage of Grammy Nominees with High Characteristic Scores')
    plt.xlabel('Characteristic')
    plt.ylabel('Percentage')
    plt.xticks(rotation=45)
    plt.ylim(0, 100)
    plt.savefig('plots/Q_3/grammy_characteristic_percent_high', bbox_inches='tight')
    plt.clf()


def artists_with_most_grammy_nominees():
    '''
    Plots a bar chart that plots the top 5 artists with the most grammy nominees
    against the number of times the artist was nominated
    '''
    df = pd.read_csv('data_organized/grammy_award_data.csv')
    df = df.dropna(subset=['artist'])

    # Splits 'artists' column into different artists and separates into separate rows
    df['artist'] = df['artist'].apply(clean_artist)
    # df = df.assign(artist=df['artist'].str.split(r'\s*[&,]\s*|\s+and\s+')
                   # ).explode('artist')
    df = df.explode('artist')
    df['artist'] = df['artist'].str.strip()

    count = df['artist'].value_counts()
    top = count.head(5)

    sns.barplot(x=top.index, y=top.values)
    plt.title('Top 5 Artists by Grammy Nominations')
    plt.xlabel('Artist')
    plt.ylabel('Number of Nominations')
    plt.xticks(rotation=45)
    plt.savefig('plots/Q_4/grammy_nominee_artists', bbox_inches='tight')
    plt.clf()


def artists_with_most_grammy_wins():
    '''
    Plots a bar chart that plots the top 5 artists with the most grammy wins
    against the number of times the artist was won
    '''
    df = pd.read_csv('data_organized/grammy_award_data.csv')

    df = df[df['winner'] == True].dropna(subset=['artist'])
    # Splits 'artists' column into different artists and separates into separate rows
    df = df.assign(artist=df['artist'].str.split(r'\s*[&,]\s*|\s+and\s+')
                ).explode('artist')
    df['artist'] = df['artist'].str.strip()

    df = df[~df['artist'].str.contains('Various', case=False)]
    top5 = df['artist'].value_counts().head(5)

    top5 = top5.reset_index()
    top5.columns = ['Artist', 'Wins']

    sns.barplot(x='Artist', y='Wins', data=top5)
    plt.title('Top 5 Grammy Winners')
    plt.xlabel('Artist')
    plt.ylabel('Number of Wins')
    plt.xticks(rotation=45)
    plt.savefig('plots/Q_4/grammy_win_artists', bbox_inches='tight')
    plt.clf()


def follower_count_against_grammy_nominations():
    '''
    Plots a scatter plot of follower count against grammy nominations for various artists
    '''
    df_nom = pd.read_csv('data_organized/grammy_award_data.csv')
    df_art = pd.read_csv('data_organized/artists.csv')

    df_nom = df_nom.dropna(subset=['artist']
                ).assign(artist=df_nom['artist'].str.split(r'\s*[&,]\s*|\s+and\s+')
                ).explode('artist')
    df_nom['artist'] = df_nom['artist'].str.strip()
    counts = df_nom['artist'].value_counts().reset_index()
    counts.columns = ['artist', 'nominations']
    df_merged = pd.merge(counts, df_art[['artist', 'followers']], on='artist')

    ax = sns.scatterplot(data=df_merged, x='nominations', y='followers', marker='o')
    # Set ticks
    max_followers = df_merged['followers'].max()
    step = 10_000_000
    yticks = list(range(0, int(max_followers + step), step))
    ylabels = [f"{int(t/1e6)}M" for t in yticks]
    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels)

    plt.title('Grammy Nominations vs. Follower Counts for Different Artists')
    plt.xlabel('Number of Grammy Nominations')
    plt.ylabel('Follower Count')
    plt.savefig('plots/Q_4/grammy_follower_counts', bbox_inches='tight')
    plt.clf()


def main():
    create_characteristic_vs_time()
    create_box_characteristic_vs_time()
    plot_characteristic_histogram()
    plot_difference_characteristic_histogram()
    char_violin_plot()
    plot_char_vs_pop()
    smoothed_char_vs_pop()
    r_value_char_bar()
    print('half')
    plot_all_characteristic_of_music()
    # grammy_characteristic_violin_plot()
    # percent_grammy_nominees_with_characteristic_plot()
    # artists_with_most_grammy_nominees()
    # artists_with_most_grammy_wins()
    # follower_count_against_grammy_nominations()
    print('done')


if __name__ == '__main__':
    main()