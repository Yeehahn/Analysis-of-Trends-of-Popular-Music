[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/teJOLcnO)


# IDP Final Project
The goal of this project is to find how and why popular/hit music has changed over time and what characteristics are typical of popular music in each time period. There has also been a smaller goal of finding if there is any notable form of bias in the Grammy Awards process. To achieve this we have found data from Spotify and the Grammy Awards to illustrate popular music and have plotted and processed it. The flow of data is rather simple as it amounts to gathering the data collected by Spotify and the Grammys, cleaning and merging the data into new csv files, and then plotting the newly processed data.

# Explanation of Folders:


**raw_data:** Contains all raw data collected for this project. Reference raw_data's README to see sources.


**plots:** All plots that were created for this project. Plots is further separated into more folders representing each question that is responded to by the plots within the folder. For more details on what the questions are reference **Discovery Document.pdf**


**data_organized:** Contains all processed datasets that are prepared for graphing.


# Files:

**cse163_utils.py:** Pre made file with functions for testing


**run_tests.py:** Runs unit tests to make sure data is being processed correctly


**prepocess_data.py:** Pre-processes data to be used in plotting


**main.py:** Creates plots and saves as files


**Discovery Document.pdf:** Planning document with background information on the project


# Instructions 
Go to the desired file and click run. All libraries are created by standard



# Challenge Goals


**Multiple Datasets:**


There were four raw datasets, artists.csv, data_by_genres.csv, grammy_award_data.csv, and spotify_datset.csv. Descriptions of all datasets can be found in the discovery document. There were 6 organized and processed datasets. artists.csv was partially merged with spotify_dataset.csv such that the average value of each characteristic (calculated by finding all music of that artist in spotify_datset.csv and averaging) of the artist's music was associated with the artist. data_by_genres.csv had a few columns filtered out. grammy_award_data.csv had several missing entries in the artist column which was resolved by merging with spotify_dataset.csv. The process was to create a dictionary of spotify_dataset.csv where the keys were a tuple of the name and year of each song and the values were the song name. Then begin iterating through every row in grammy_award_data.csv and for every value without an artist try finding the corresponding song using the created dictionary and assign it to the row. However, this was insufficient because awards that go to performances or albums could not be attributed to any artist and left several Nan values. Furthermore, since all grammy's sometimes ocurr a year after the song was created there was a tolerance of 1 year for which songs to check for. At this point the naming of artists for grammy_award_data.csv is still inconsistent and for our analysis more cleaning needed to be done. The dataset concatenates multiple artist together with either a comma, &, featured, or "and". Furthermore, for performances it will only *sometimes* say the original songwriters name in parentheses. Thus, it was needed to create a list which splits according to all of the mentioned delimiters and ignore everything within parentheses. However, grammy_award_data also *sometimes* attributes role to artists names (engineer, producer, remixer, etc.) and these role names needed to be ignored so a set including all phrases/titles to be ignored was created. The dataset has so many role names that it was extremely difficult to remove all of them but we managed to catch and remove the most prevalent ones so that it does not interfere with our analysis of who is winning with grammy awards. Only at this point was cleaning finished and that created grammy_award_data.csv in data_organized. grammy_song_char.csv was created by merging grammy_award_data.csv and spotify_dataset.csv was merged to associated songs with their respective characteristics. spotify_dataset.csv had a few columns filtered and was filtered by popularity. Whatever was filtered as popular went to spotify_dataset.csv and whatever wasn't went to unpopular_music.csv.


**Statistical Validation:**
To verify and qualify the correlation found here we used Pandas method df.corr(method=’pearson’) to calculate the r-value of each characteristic. The correlation method was done on a non-averaged/non-grouped dataset. This allows for accurate calculations whereas if we computed the r-values with the grouped version shown in the characteristic vs. popularity graph it would have unnaturaly high values. The results can be seen below:
| Characteristic | r-value |
| ------------ | --------|
| Acousticness | -0.573162 |
| Danceability | 0.199606 |
| Energy  | 0.485005 |
| Instrumentalness | -0.296750 |
| Liveness | -0.076464 |
| Speechiness | -0.171979 |
| Valence  | 0.014200 |


While there are no characteristics with extremely strong correlation coefficients (r-values > 0.7), acousticness and energy have moderately strong correlations. Suggesting more electric or less acoustic music and more energetic music is typically a differing factor between popular music and unpopular music. 

To analyze if the Grammy's are biased we performed a chi-square goodness of fit test on the number of wins an artist has compared to the numebr of nominations. Artists that we took interest to were Beyoncé (99 nominations 35 wins) and Brian Mcknight (17 nominations 0 wins).

Before continuing the test we must dicuss and define what would indicate a "bias" in selection. The first obvious approach would be to treat the chances of winning once an artist is nominated as random (there are typically 5 nominees so a 20% chance of winning). However, that would be assuming that an artist's music isn't simply *better* or *worse* than all other nominees. Thus, we will perform the test 3 times for both artist. We will arbitrarily select the odds of winning if their music is worse on average as being 15%, if the same on average as being 20%, and if better on average as being 25%. While these values are arbitrarily selected it should still partially account for winning being a result of greater quality rather than bias in selection. 

**Beyconé analysis:**

Null Hypothesis H~0~: There is no bias in Grammy wins for Beyoncé

Alternative Hypothesis H~A~: There is a bias in Grammy wins for Beyoncé

Worse:
| Outcome | Observed (O) | Expected (E) |
| ------- | ------------ | ------------ |
| Wins | 35 | 0.15 * 99 (14.85) |
| Losses | 64 | 0.85 * 99 (84.15) |

Equal:

| Outcome | Observed (O) | Expected (E) |
| ------- | ------------ | ------------ |
| Wins | 35 | 0.2 * 99 (19.8) |
| Losses | 64 | 0.8 * 99 (79.2) |


Better:

| Outcome | Observed (O) | Expected (E) |
| ------- | ------------ | ------------ |
| Wins | 35 | 0.25 * 99 (24.75) |
| Losses | 64 | 0.75 * 99 (74.25) |

**Conditions:**
Random-sampling is not applicable for this scenario.
Results are not independent because sometimes singular pieces of music (albums or songs) are nominated for multiple awards. We will continue with caution.
All category values greater than 5.

**Results:**
We will set our alpha-level = 0.05 as this is standard.

Worse: χ² = 32.167 p < 0.00001

Equal: χ² = 14.586 p = 0.00013

Better: χ² = 5.66 p = 0.01736

For all 3 cases the p-value was significantly lower than 0.05. Therefore we can reject the null hypothesis, there is statistically significant evidence to suggest that there is a bias favoring Beyoncé when selecting the winner for a Grammy award.


**Brian Mcknight analysis:**

Null Hypothesis H~0~: There is no bias in Grammy wins for Brian Mcknight

Alternative Hypothesis H~A~: There is a bias in Grammy wins for Brian Mcknight

Worse:
| Outcome | Observed (O) | Expected (E) |
| ------- | ------------ | ------------ |
| Wins | 0 | 0.15 * 17 (2.55) |
| Losses | 17 | 0.85 * 17 (14.45) |

Equal:

| Outcome | Observed (O) | Expected (E) |
| ------- | ------------ | ------------ |
| Wins | 0 | 0.2 * 17 (3.4) |
| Losses | 17 | 0.8 * 17 (13.6) |


Better:

| Outcome | Observed (O) | Expected (E) |
| ------- | ------------ | ------------ |
| Wins | 0 | 0.25 * 17 (4.25) |
| Losses | 17 | 0.75 * 17 (12.75) |

**Conditions:**
Random-sampling is not applicable for this scenario.
Results are not independent because sometimes singular pieces of music (albums or songs) are nominated for multiple awards. We will continue with caution.
Not all category values are greater than 5, but in this case it should not be significant. Nonetheless, we will continue with caution.

**Results:**

We will set our alpha-level = 0.05 as this is standard.

Worse: χ² = 3 p = 0.08326

Equal: χ² = 4.25 p = 0.03925

Better: χ² = 5.667 p = 0.01729

For only two cases (equal and better) was the p-value lower than the alphal-level. Due to the unfulfilled conditions and p-value in the worse scenario, there is insufficient statistical evidence to reject the null hypothesis, there appears to be no bias substantial bias in the selection of winning a Grammy for Brian Mcknight.
