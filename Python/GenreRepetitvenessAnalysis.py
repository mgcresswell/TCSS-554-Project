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
query = "select Genre, HIndex from MetroLyrics m inner join  MetroLyricHIndex h on m.MetroLyricId = h.MetroLyricId "
songsDf = pd.read_sql(query, connection)
averageDf = songsDf.groupby("Genre").mean()

height = averageDf[['HIndex']].to_numpy().ravel() 
bars = averageDf.index.values
y_pos = np.arange(len(bars))
figure(num=None, figsize=(10, 4), dpi=200, facecolor='w', edgecolor='k')
plt.bar(y_pos, height, color=mcolors.TABLEAU_COLORS)
plt.title('Average HP-Point By Genre')
plt.xlabel('Genre')
plt.ylabel('HP-Point')
plt.xticks(y_pos, bars,rotation=25)
plt.savefig('GenreRepetitveness_HIndex.png')
plt.show()



connection = db.GetCloudConnection()
query = "select Genre, HIndex from MetroLyrics m inner join StemmedMetroLyricHIndex h on m.MetroLyricId = h.MetroLyricId "
songsDf = pd.read_sql(query, connection)
averageDf = songsDf.groupby("Genre").mean()

height = averageDf[['HIndex']].to_numpy().ravel() 
bars = averageDf.index.values
y_pos = np.arange(len(bars))
figure(num=None, figsize=(10, 4), dpi=200, facecolor='w', edgecolor='k')
plt.bar(y_pos, height, color=mcolors.TABLEAU_COLORS)
plt.title('Average Stemmed HP-Point by Genre')
plt.xlabel('Genre')
plt.ylabel('Stemmed HP-Point')
plt.xticks(y_pos, bars,rotation=25)
plt.savefig('GenreRepetitveness_StemmedHIndex.png')
plt.show()
