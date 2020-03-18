import numpy as np
import matplotlib.pyplot as plt
import pymysql
import pymysql.cursors
import spacy 
import pandas as pd
import DbFunctions as db
from matplotlib.pyplot import figure
import matplotlib.colors as mcolors

connection = db.GetCloudConnection()
query = "SELECT c.*, s.Genre FROM lyrics.MetroLyricsComplexityIndex c inner join lyrics.MetroLyrics s on s.MetroLyricId = c.SongId;  "
songsDf = pd.read_sql(query, connection)

metricDf = songsDf[['SentenceCount','WordCount','AvgSyllablesPerWord','AvgSentenceLength','DifficultWordCount','SyllableCount','GunningFog','PolySyllable','SmogIndex','DaleChall','Flesch','Genre']]
averageDf = metricDf.groupby("Genre").mean()


height = averageDf[['SentenceCount']].to_numpy().ravel() 
bars = averageDf.index.values
y_pos = np.arange(len(bars))
figure(num=None, figsize=(10, 4), dpi=200, facecolor='w', edgecolor='k')
plt.bar(y_pos, height, color=mcolors.TABLEAU_COLORS)
plt.title('Average Number of Senctences By Genre')
plt.xlabel('Genre')
plt.ylabel('Average Sentence Count')
plt.xticks(y_pos, bars,rotation=25)
plt.savefig('GenreComplexity_SentenceCount.png')
plt.show()


wordCounts = averageDf[['WordCount']].to_numpy().ravel() 
bars = averageDf.index.values
y_pos = np.arange(len(bars))
figure(num=None, figsize=(10, 4), dpi=200, facecolor='w', edgecolor='k')
plt.bar(y_pos, wordCounts, color=mcolors.TABLEAU_COLORS)
plt.title('Average Word Count By Genre')
plt.xlabel('Genre')
plt.ylabel('Word Count')
plt.xticks(y_pos, bars,rotation=25)
plt.savefig('GenreComplexity_WordCount.png')
plt.show()


height = averageDf[['AvgSyllablesPerWord']].to_numpy().ravel() 
bars = averageDf.index.values
y_pos = np.arange(len(bars))
figure(num=None, figsize=(10, 4), dpi=200, facecolor='w', edgecolor='k')
plt.bar(y_pos, height, color=mcolors.TABLEAU_COLORS)
plt.title('Average Syllables Per Word By Genre')
plt.xlabel('Genre')
plt.ylabel('Syllables Per Word')
plt.xticks(y_pos, bars,rotation=25)
plt.savefig('GenreComplexity_AvgSyllablesPerWord.png')
plt.show()

height = averageDf[['AvgSentenceLength']].to_numpy().ravel() 
bars = averageDf.index.values
y_pos = np.arange(len(bars))
figure(num=None, figsize=(10, 4), dpi=200, facecolor='w', edgecolor='k')
plt.bar(y_pos, height, color=mcolors.TABLEAU_COLORS)
plt.title('Average Sentence Length By Genre')
plt.xlabel('Genre')
plt.ylabel('Sentence Length')
plt.xticks(y_pos, bars,rotation=25)
plt.savefig('GenreComplexity_AvgSentenceLength.png')
plt.show()


difficultWords = averageDf[['DifficultWordCount']].to_numpy().ravel() 
percentOfDifficultWords = np.divide(difficultWords,wordCounts)
bars = averageDf.index.values
y_pos = np.arange(len(bars))
figure(num=None, figsize=(10, 4), dpi=200, facecolor='w', edgecolor='k')
plt.bar(y_pos, percentOfDifficultWords, color=mcolors.TABLEAU_COLORS)
plt.title('Percent of Difficult Words By Genre')
plt.xlabel('Genre')
plt.ylabel('% of Difficult Words')
plt.xticks(y_pos, bars,rotation=25)
plt.savefig('GenreComplexity_PercentofDifficultWords.png')
plt.show()


gunningFog = averageDf[['GunningFog']].to_numpy().ravel() 
bars = averageDf.index.values
y_pos = np.arange(len(bars))
figure(num=None, figsize=(10, 4), dpi=200, facecolor='w', edgecolor='k')
plt.bar(y_pos, gunningFog, color=mcolors.TABLEAU_COLORS)
plt.title('Average Gunning Fog by Genre')
plt.xlabel('Genre')
plt.ylabel('Average Gunning Fog')
plt.xticks(y_pos, bars,rotation=25)
plt.savefig('GenreComplexity_AverageGunningFog.png')
plt.show()


pollySyllable = averageDf[['PolySyllable']].to_numpy().ravel() 
bars = averageDf.index.values
y_pos = np.arange(len(bars))
figure(num=None, figsize=(10, 4), dpi=200, facecolor='w', edgecolor='k')
plt.bar(y_pos, pollySyllable, color=mcolors.TABLEAU_COLORS)
plt.title('Average PollySyllable By Genre')
plt.xlabel('Genre')
plt.ylabel('Average PollySyllable')
plt.xticks(y_pos, bars,rotation=25)
plt.savefig('GenreComplexity_PollySyllable.png')
plt.show()


smogIndex = averageDf[['SmogIndex']].to_numpy().ravel() 
bars = averageDf.index.values
y_pos = np.arange(len(bars))
figure(num=None, figsize=(10, 4), dpi=200, facecolor='w', edgecolor='k')
plt.bar(y_pos, smogIndex, color=mcolors.TABLEAU_COLORS)
plt.title('Average Smog Index by Genre')
plt.xlabel('Genre')
plt.ylabel('Average Smog Index')
plt.xticks(y_pos, bars,rotation=25)
plt.savefig('GenreComplexity_SmogIndex.png')
plt.show()

dalechall = averageDf[['DaleChall']].to_numpy().ravel() 
bars = averageDf.index.values
y_pos = np.arange(len(bars))
figure(num=None, figsize=(10, 4), dpi=200, facecolor='w', edgecolor='k')
plt.bar(y_pos, dalechall, color=mcolors.TABLEAU_COLORS)
plt.title('Average Dale Chall by Genre')
plt.xlabel('Genre')
plt.ylabel('Average Dale Chall')
plt.xticks(y_pos, bars,rotation=25)
plt.savefig('GenreComplexity_DaleChall.png')
plt.show()


flesch = averageDf[['Flesch']].to_numpy().ravel() 
bars = averageDf.index.values
y_pos = np.arange(len(bars))
figure(num=None, figsize=(10, 4), dpi=200, facecolor='w', edgecolor='k')
plt.bar(y_pos, flesch, color=mcolors.TABLEAU_COLORS)
plt.title('Average Flesch by Genre')
plt.xlabel('Genre')
plt.ylabel('Average Flesch')
plt.xticks(y_pos, bars,rotation=25)
plt.savefig('GenreComplexity_Flesch.png')
plt.show()
t =0