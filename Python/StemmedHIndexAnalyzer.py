import numpy as np
import matplotlib.pyplot as plt
import pymysql
import pymysql.cursors
import pandas as pd
import DbFunctions as db
from matplotlib.pyplot import figure


connection = db.GetCloudConnection()
songs = db.GetStemmedHIndexData(connection)
gr = songs.groupby('Year').agg({'HIndex': ['mean']}).reset_index()

x = gr[['Year']].to_numpy().ravel() 
y = gr[['HIndex']].to_numpy().ravel() 


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
plt.title('Average Stemmed Billboard Top 100 HP-Point by Year')
plt.xlabel('Year')
plt.ylabel('Average HP-Point')
plt.xticks(x, yearLabels,rotation=45, ha="left",fontsize=8)
plt.xticks()
plt.savefig('StemmedHIndex.png')
plt.show()
y = 0