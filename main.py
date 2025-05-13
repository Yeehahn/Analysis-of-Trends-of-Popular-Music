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


def create_characteristic_vs_time():
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
        adjust_plot_characteristic(characteristic, 'plots/characteristic_vs_time/',
                                   '_vs_time_reg')

    for characteristic in characteristic_not_100_range:
        sns.regplot(x=spot_df.index, y=characteristic, data=spot_df)
        adjust_plot_characteristic(characteristic, 'plots/characteristic_vs_time/',
                                   '_vs_time_reg')
    plt.clf()


def create_box_characteristic_vs_time():
    sns.set()
    spot_df = load_spot_df_for_char()
    characteristic_100_range = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                                'liveness', 'speechiness', 'valence']
    characteristic_not_100_range = ['duration_ms', 'loudness', 'tempo']

    for characteristic in characteristic_100_range:
        sns.boxplot(x='decade', y=characteristic, data=spot_df, showfliers=False)
        plt.ylim((0, 100))
        adjust_plot_characteristic(characteristic, 'plots/characteristic_vs_time/',
                                   '_vs_time_box')

    for characteristic in characteristic_not_100_range:
        sns.boxplot(x='decade', y=characteristic, data=spot_df, showfliers=False)
        adjust_plot_characteristic(characteristic, 'plots/characteristic_vs_time/',
                                   '_vs_time_box')
    plt.clf()


def adjust_plot_characteristic(characteristic, folder_path, title):
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
                       'liveness', 'speechiness', 'valence']]


def plot_characteristic_histogram():
    sns.set()
    spot_df = load_spot_df_for_char()
    spot_df = spot_df[(spot_df['decade'] >= 1990) & (spot_df['decade'] < 2020)]
    characteristic_100_range = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                                'liveness', 'speechiness', 'valence']
    decade_char = spot_df.groupby('decade')[characteristic_100_range].mean()

    x_axis = np.arange(3)
    bar_width = 0.1
    fig, ax = plt.subplots(figsize=(14, 6))

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
    spot_df = load_spot_df_for_char()
    spot_df = spot_df[(spot_df['decade'] >= 1990) & (spot_df['decade'] < 2020)]
    characteristic_100_range = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                                'liveness', 'speechiness', 'valence']
    spot_tot_df = pd.read_csv('raw_data/spotify_dataset_clean.csv')
    spot_tot_df = spot_tot_df.drop(['name', 'artists'], axis=1)
    spot_tot_df['decade'] = spot_tot_df['year'].floordiv(10).mul(10)
    spot_tot_df = spot_tot_df[(spot_tot_df['decade'] >= 1990) & (spot_tot_df['decade'] < 2020)]

    decade_pop_char = spot_df.groupby('decade')[characteristic_100_range].mean()
    decade_tot_char = spot_tot_df.groupby('decade')[characteristic_100_range].mean() * 100
    decade_char = decade_pop_char - decade_tot_char

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
    plt.title('Characteristics of Popular - All Music by Decade')
    plt.ylim(-50, 50)
    plt.legend()
    plt.savefig('plots/Q_2/characteristic_difference_histogram', bbox_inches='tight')
    plt.clf()


def load_spot_df_for_char():
    spot_df = pd.read_csv('data_organized/spotify_dataset.csv')
    spot_df = spot_df.drop(['name', 'artists'], axis=1)
    spot_df['decade'] = spot_df['year'].floordiv(10).mul(10)
    return spot_df


def char_violin_plot():
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


def main():
    # create_characteristic_vs_time()
    # create_box_characteristic_vs_time()
    # plot_characteristic_histogram()
    plot_difference_characteristic_histogram()
    # char_violin_plot()
    # plot_char_vs_pop()
    # smoothed_char_vs_pop()
    r_value_char_bar()


if __name__ == '__main__':
    main()