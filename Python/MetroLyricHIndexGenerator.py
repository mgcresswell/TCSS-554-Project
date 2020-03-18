import numpy as np
import pymysql
import pymysql.cursors
import pandas as pd
import DbFunctions as db

def Tokenize(row):
    tokens = []
    for w in row['ProcessedLyrics'].split():
        tokens.append(w)
    return tokens

def hIndex(citations):
        n = len(citations)
        equal_h = [0] * (n+1)
        for h in range(n):
            if citations[h] >= n: equal_h[n] += 1
            else: equal_h[citations[h]] += 1     
        s = 0
        for h in range(n,0, -1):
            s += equal_h[h]
            if s>=h:
                return h          
        return 0

def GroupTokens(tokens):
    repIndex = []
    df = pd.DataFrame(data=tokens, columns=['tokens'])
    gk = df.groupby('tokens').size().to_frame('size')
    gk = gk.reset_index()
    sgk = gk.sort_values(by='size', ascending=False)
    citations = np.array(sgk['size'])
    hindex = hIndex(citations)
    return hindex



connection = db.GetCloudConnection()
songs = db.GetMetroSongs(connection, "")
repIndex = []

for index, row in songs.iterrows(): 
    tokens = Tokenize(row)
    repIndex.append([row['MetroLyricId'],GroupTokens(tokens)])


newconnection = db.GetCloudConnection()
with newconnection.cursor() as cursor:
       for i in range(len(repIndex)):
           sql = "INSERT INTO MetroLyricHIndex (MetroLyricId, HIndex) VALUES (%s,%s) "
           cursor.execute(sql, (str(repIndex[i][0]),str(repIndex[i][1])))
           newconnection.commit()
cursor.close();
