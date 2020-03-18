import numpy as np
import matplotlib.pyplot as plt
import pymysql
import pymysql.cursors
import pandas as pd
import DbFunctions as db
from matplotlib.pyplot import figure


connection = db.GetCloudConnection()
query = "select s.SongId, Year, HIndex from lyrics.songs s inner join lyrics.HIndex h on s.SongId = h.SongId "
songsDf = pd.read_sql(query, connection)
genres = ['rock','pop','rap','rnb','soul','dance','country','alternative','funk','Disco','jazz','electronic','folk','indie']

t = []
for index, row in songsDf.iterrows():
    tagQuery = "select Tag from lyrics.songTags Where SongId = " + str(row['SongId'])
    tags = pd.read_sql(tagQuery, connection).to_numpy()

    for index2, row2 in tags.iterrows():
        for i in range(len(genres)):
            if (row2['Tag'] == genres[i]):
                t.append([row['HIndex'],row2['Tag'],row['Year']])


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
plt.title('Average Billboard Top 100 HP-Point by Year')
plt.xlabel('Year')
plt.ylabel('Average HP-Point')
plt.xticks(x, yearLabels,rotation=45, ha="left",fontsize=4)
plt.savefig('HIndex.png')
plt.show()
y = 0
