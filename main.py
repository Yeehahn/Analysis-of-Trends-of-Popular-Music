'''
Create amazing plots in this file. You will read the data from `data_organized` 
(unless your raw data required no reduction, in which case you can read your data from `raw_data`). 
You will do plot-related work such as joins, column filtering, pivots, 
small calculations and other simple organizational work. 
'''
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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


def create_box_characteristic_vs_time():
    sns.set()
    spot_df = pd.read_csv('data_organized/spotify_dataset.csv')
    spot_df = spot_df.drop(['name', 'artists'], axis=1)
    spot_df['decade'] = spot_df['year'].floordiv(10).mul(10)
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


def main():
    # create_characteristic_vs_time()
    create_box_characteristic_vs_time()


if __name__ == '__main__':
    main()