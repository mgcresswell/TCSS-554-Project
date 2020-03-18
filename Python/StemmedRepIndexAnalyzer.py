import numpy as np
import matplotlib.pyplot as plt
import pymysql
import pymysql.cursors
import pandas as pd
import DbFunctions as db
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

connection = db.GetCloudConnection()
repIndex = db.GetStemmedRepIndex(connection)

totalsDf = repIndex.groupby('SongId').agg({'Count': ['sum']}).reset_index()
filteredRepIndex = repIndex[repIndex['Count'] > 1]
filterdDf = filteredRepIndex.groupby('SongId').agg({'Count': ['sum']}).reset_index()

metric = []
for index, row in totalsDf.iterrows(): 
    countRow = filterdDf[filterdDf['SongId'] == row[0]]
    countRow = countRow.to_numpy().ravel() 
    if len(countRow) > 0:
        year = repIndex[repIndex['SongId'] == row[0]]
        year = year.to_numpy().ravel()    
        metric.append([countRow[0],year[1],countRow[1]/row[1]])

metricDf = pd.DataFrame(data=metric, columns=['SongId','Year','Metric'])
gr = metricDf.groupby('Year').agg({'Metric': ['mean']}).reset_index()

x = gr[['Year']].to_numpy().ravel() 
y = gr[['Metric']].to_numpy().ravel() 

yearLabels = []
for i in range(len(x)):
    if (i % 2) == 0:
        yearLabels.append(str(x[i]))
    else:
        yearLabels.append("")

xi = list(range(len(x)))
figure(num=None, figsize=(14, 6), dpi=200, facecolor='w', edgecolor='k')
plt.scatter(x, y)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
plt.title('Average Billboard Top 100 Stemmed Repetitve Word Probabilty by Year')
plt.xlabel('Year')
plt.ylabel('Repetitive Word Probablility')
plt.xticks(x, yearLabels,rotation=45, ha="left",fontsize=8)
plt.xticks()
plt.savefig('StemmedRepetitionIndex.png')
plt.show()
y = 0

