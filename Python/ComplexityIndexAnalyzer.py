import numpy as np
import matplotlib.pyplot as plt
import pymysql
import pymysql.cursors
import spacy 
import pandas as pd
import DbFunctions as db
from matplotlib.pyplot import figure


connection = db.GetCloudConnection()
query = "SELECT c.*, s.Year FROM lyrics.ComplexityIndex c inner join lyrics.songs s on s.SongId = c.SongId; "
songsDf = pd.read_sql(query, connection)

metricDf = songsDf[['SentenceCount','WordCount','AvgSyllablesPerWord','AvgSentenceLength','DifficultWordCount','SyllableCount','GunningFog','PolySyllable','SmogIndex','DaleChall','Flesch','Year']]
averageDf = metricDf.groupby("Year").mean()
wordCounts = averageDf[['WordCount']].to_numpy().ravel() 
x = averageDf.index.values

yearLabels = []
for i in range(len(x)):
    if (i % 2) == 0:
        yearLabels.append(str(x[i]))
    else:
        yearLabels.append("")

figure(num=None, figsize=(14, 6), dpi=200, facecolor='w', edgecolor='k')
plt.scatter(x, wordCounts)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, wordCounts, 1))(np.unique(x)))
plt.title('Average Billboard Top 100 Word Count by Year')
plt.xlabel('Year')
plt.ylabel('Word Count')
plt.xticks(x, yearLabels,rotation=45, ha="left",fontsize=8)
plt.savefig('BillBoardComplexityIndex_WordCount.png')
plt.show()
y = 0


y = averageDf[['SentenceCount']].to_numpy().ravel() 
figure(num=None, figsize=(14, 6), dpi=200, facecolor='w', edgecolor='k')
plt.scatter(x, y)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
plt.title('Average Billboard Top 100 Sentence Count by Year')
plt.xlabel('Year')
plt.ylabel('Sentence Count')
plt.xticks(x, yearLabels,rotation=45, ha="left",fontsize=8)
plt.savefig('BillBoardComplexityIndex_SentenceCount.png')
plt.show()
y = 0


y = averageDf[['AvgSyllablesPerWord']].to_numpy().ravel() 
figure(num=None, figsize=(14, 6), dpi=200, facecolor='w', edgecolor='k')
plt.scatter(x, y)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
plt.title('Average Billboard Top 100 Average Syllables Per Word by Year')
plt.xlabel('Year')
plt.ylabel('Average Syllables Per Word')
plt.xticks(x, yearLabels,rotation=45, ha="left",fontsize=8)
plt.savefig('BillBoardComplexityIndex_AvgSyllablesPerWord.png')
plt.show()
y = 0


y = averageDf[['AvgSentenceLength']].to_numpy().ravel() 
figure(num=None, figsize=(14, 6), dpi=200, facecolor='w', edgecolor='k')
plt.scatter(x, y)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
plt.title('Average Billboard Top 100 Average Sentence Length by Year')
plt.xlabel('Year')
plt.ylabel('Average Sentence Length')
plt.xticks(x, yearLabels,rotation=45, ha="left",fontsize=8)
plt.savefig('BillBoardComplexityIndex_AvgSentenceLength.png')
plt.show()
y = 0


y = averageDf[['DifficultWordCount']].to_numpy().ravel() 
y = np.divide(y,wordCounts)
figure(num=None, figsize=(14, 6), dpi=200, facecolor='w', edgecolor='k')
plt.scatter(x, y)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
plt.title('Percent of Difficult Words by Year')
plt.xlabel('Year')
plt.ylabel('Percent of Difficult Words')
plt.xticks(x, yearLabels,rotation=45, ha="left",fontsize=8)
plt.savefig('BillBoardComplexityIndex_PercentOfDifficultWords.png')
plt.show()
y = 0


y = averageDf[['GunningFog']].to_numpy().ravel() 
figure(num=None, figsize=(14, 6), dpi=200, facecolor='w', edgecolor='k')
plt.scatter(x, y)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
plt.title('Average Gunning Fog by Year')
plt.xlabel('Year')
plt.ylabel('Gunning Fog')
plt.xticks(x, yearLabels,rotation=45, ha="left",fontsize=8)
plt.savefig('BillBoardComplexityIndex_GunningFog.png')
plt.show()
y = 0


y = averageDf[['PolySyllable']].to_numpy().ravel() 
figure(num=None, figsize=(14, 6), dpi=200, facecolor='w', edgecolor='k')
plt.scatter(x, y)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
plt.title('Average PolySyllable by Year')
plt.xlabel('Year')
plt.ylabel('PolySyllable')
plt.xticks(x, yearLabels,rotation=45, ha="left",fontsize=8)
plt.savefig('BillBoardComplexityIndex_PolySyllable.png')
plt.show()
y = 0


y = averageDf[['SmogIndex']].to_numpy().ravel() 
figure(num=None, figsize=(14, 6), dpi=200, facecolor='w', edgecolor='k')
plt.scatter(x, y)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
plt.title('Average SmogIndex by Year')
plt.xlabel('Year')
plt.ylabel('SmogIndex')
plt.xticks(x, yearLabels,rotation=45, ha="left",fontsize=8)
plt.savefig('BillBoardComplexityIndex_SmogIndex.png')
plt.show()
y = 0

y = averageDf[['DaleChall']].to_numpy().ravel() 
figure(num=None, figsize=(14, 6), dpi=200, facecolor='w', edgecolor='k')
plt.scatter(x, y)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
plt.title('Average DaleChall by Year')
plt.xlabel('Year')
plt.ylabel('DaleChall')
plt.xticks(x, yearLabels,rotation=45, ha="left",fontsize=8)
plt.savefig('BillBoardComplexityIndex_DaleChall.png')
plt.show()
y = 0

y = averageDf[['Flesch']].to_numpy().ravel() 
figure(num=None, figsize=(14, 6), dpi=200, facecolor='w', edgecolor='k')
plt.scatter(x, y)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
plt.title('Average Flesch by Year')
plt.xlabel('Year')
plt.ylabel('Flesch')
plt.xticks(x, yearLabels,rotation=45, ha="left",fontsize=8)
plt.savefig('BillBoardComplexityIndex_Flesch.png')
plt.show()
y = 0