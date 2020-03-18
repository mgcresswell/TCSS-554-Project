import lyricsgenius
import pymysql;
import pandas as pd;
import DbFunctions as db
import matplotlib.pyplot as plt

def getProfaneWords():
    stopwordsFile = "C:\\Users\\cressm\\Desktop\\TCSS 554\\profanity.txt"
    stopwords = []
    with open(stopwordsFile, "r") as f:
       for line in f:
         stopwords.extend(line.split())
    return stopwords


connection = db.GetCloudConnection()
repIndex = db.GetRepIndexGroupedByYearToken(connection)

metric = []
profaneWords = getProfaneWords()
for index, row in repIndex.iterrows(): 
    #if index < 1000:
        for word in profaneWords:
            if row[1] == word:
                metric.append([row[0],row[2]])
    #else:
    #    break 


metric2 = []
yearTotals = repIndex.groupby('Year').agg({'Count': ['sum']}).reset_index()
metricDf = pd.DataFrame(data=metric, columns=['Year','Count'])
for index, row in metricDf.iterrows(): 
    total = yearTotals[yearTotals['Year'] == row['Year']]
    total = total['Count'].to_numpy().ravel() 
    metric2.append([row[0], row[1]/total[0]])


metricDf = pd.DataFrame(data=metric2, columns=['Year','Count'])
gr = metricDf.groupby('Year').agg({'Count': ['mean']}).reset_index()

x = gr[['Year']].to_numpy().ravel() 
y = gr[['Count']].to_numpy().ravel() 

colors = (0,0,0)
plt.plot(x, y)
plt.title('Scatter plot pythonspot.com')
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('foo2.png')
plt.show()
y = 0