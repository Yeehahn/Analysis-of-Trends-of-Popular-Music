This will contain data that is small enough for consumption and ready to be plotted. If the raw data from the data sources is dirty or too big for quick and repeated consumption, you need to reduce, normalize and organize the data first. Store the raw data in the raw_data folder. After you've cleaned and organized it, save the processed data into this folder. However, if the raw data is clean and small enough, and it does not need any preprocesssing, you can store the raw data here.  

**Sources for data:**
**artist.csv**: https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-1921-2020-160k-tracks?resource=download & https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks
**data_by_genres.csv**:  https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-1921-2020-160k-tracks?select=data_by_genres.csv
**grammy_song_char.csv**: https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-1921-2020-160k-tracks?resource=download & https://observablehq.com/@uw-info474/exploratory-data-analysis-of-various-music-datasets 
**grammy_award_data.csv**: https://observablehq.com/@uw-info474/exploratory-data-analysis-of-various-music-datasets 
**spotify_dataset.csv**: https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-1921-2020-160k-tracks?resource=download

**Desriptions:**
**artist.csv**: Each entry in this dataset represents a popular artist on Spotify. It contains general information on the artist, what genre of music the artist creates, and what the characteristics of the artist’s music are. 
**data_by_genres.csv**:  Each entry in this dataset represents a genre of music and all of the ML generated characteristics. Overall, this is the exact same as the raw dataset but two unnecessary columns were removed. 
**grammy_song_char.csv**: Each entry in this dataset represents a song that earned a grammy and all of the Spotify ML generated characteristics that the song has. 
**grammy_award_data.csv**: This dataset contains all Grammy awards and nominations given from 1966-2025. This dataset is a cleaned version (removed unnecessary columns) of the raw one.
**spotify_dataset.csv**:Each entry in this dataset is a song and the song’s relevant information from the time frame of 1921-2020. Each entry contains basic information such as song name, artist, year of release, tempo, etc. However, the most important data for our project will be Spotify's ML generated measurements of certain qualities of songs. All songs in this dataset are loosely considered *popular* by using the popularity column.
