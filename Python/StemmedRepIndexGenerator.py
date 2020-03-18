import pymysql
import pymysql.cursors
import spacy 
import pandas as pd
import DbFunctions as db


# Create Reptitivness Index
connection = db.GetCloudConnection()
query = "select SongId, StemmedLyrics from songs where StemmedLyrics is not null and SongId not in (SELECT distinct SongId FROM lyrics.StemmedRepIndex);"
songsDf = pd.read_sql(query, connection)

repIndex = []
for index, row in songsDf.iterrows(): 
    tokens = []
    for w in row['StemmedLyrics'].split():
        tokens.append(w)

    df = pd.DataFrame(data=tokens, columns=['tokens'])
    gk = df.groupby('tokens').size().reset_index()
    for index2, row2 in gk.iterrows(): 
        repIndex.append([row['SongId'], row2['tokens'],row2[0]])

newconnection = db.GetCloudConnection()
with newconnection.cursor() as cursor:
       for i in range(len(repIndex)):
           sql = "INSERT INTO StemmedRepIndex (SongId,Token,Count) VALUES (%s,%s,%s) "
           cursor.execute(sql, (str(repIndex[i][0]),str(repIndex[i][1]), str(repIndex[i][2])))
           newconnection.commit()
cursor.close()
connection.close()