'''
This is the entry point to running all of your tests. 
You can do simple testing as we have done all year in your homework assignments. 
Or, you can leverage Python's Unit Test Framework which is a bit more complicated, but super cool.  

A common command to run the unit tests from the console is: python -m unittest discover -s tests -v

Your tests would all inherit from unittest.TestCase.

Take advantage of helper function in cse163_utils.py to help you with testing.
'''
import unittest
import pandas as pd


class TestData(unittest.TestCase):

    def test_fill_artist(self):
        '''
        The data isn't perfectly clean 
        with consistent capitalization, marking of correct artists, and song names
        Bad Guy has different capitalization and the years are off
        This makes sure that fill_artist is accounting for both of those
        '''
        grammy = pd.read_csv('data_organized/grammy_award_data.csv')
        best_song = grammy['category'] == 'Song Of The Year'
        year = grammy['year'] == 2020
        song = grammy['nominee'] == 'Bad Guy'
        row = grammy[best_song & year & song]
        self.assertEqual(row['artist'].iloc[0], 'Billie Eilish')

    def test_grammy_song_char(self):
        '''
        Once again Bad Guy's name creates errors with filters
        It also is an album so this makes sure that albums are being dropped
        '''
        grammy = pd.read_csv('data_organized/grammy_song_char.csv')
        year = grammy['year'] == 2019
        song = grammy['nominee'] == 'Bad Guy'
        row = grammy[year & song]
        self.assertEqual(row['category'].iloc[0], 'Song Of The Year')

    def test_grammy_song_category(self):
        '''
        Once again Bad Guy's name creates errors with filters
        It also is an album so this makes sure that albums are being dropped
        '''
        grammy = pd.read_csv('data_organized/grammy_song_char.csv')
        year = grammy['year'] == 2019
        song = grammy['nominee'] == 'Bad Guy'
        row = grammy[year & song]
        self.assertEqual('album' not in row['category'], True)