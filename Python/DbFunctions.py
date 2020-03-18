import pymysql;
import pandas as pd;


def GetCloudConnection():
    connection = pymysql.connect(host='35.233.229.223',
                             user='cressm',
                             password='Welcome1234!',
                             db='lyrics',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    return connection


def GetLocalConnection():
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Seattle1234!',
                             db='lyrics',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    return connection

def GetSongs(connection, where):
       query = "select * from lyrics.songs " + where
       df = pd.read_sql(query, connection)
       connection.close()
       return df

def GetMetroSongs(connection, where):
       query = "select MetroLyricId, ProcessedLyrics from lyrics.MetroLyrics " + where
       df = pd.read_sql(query, connection)
       connection.close()
       return df

def GetRepIndex(connection):
       query = "SELECT s.SongId, s.Year, r.Count, r.Token FROM lyrics.songs s inner join lyrics.RepIndex r on s.SongId = r.SongId;"
       df = pd.read_sql(query, connection)
       connection.close()
       return df

def GetStemmedRepIndex(connection):
       query = "SELECT s.SongId, s.Year, r.Count, r.Token FROM lyrics.songs s inner join lyrics.StemmedRepIndex r on s.SongId = r.SongId;"
       df = pd.read_sql(query, connection)
       connection.close()
       return df

def GetRepIndexGroupedByYearToken(connection):
       query = "SELECT Year, Token, Sum(Count) as Count FROM lyrics.RepIndex r inner join lyrics.songs s on r.SongId = s.SongId group by Year, Token;"
       df = pd.read_sql(query, connection)
       connection.close()
       return df

def GetHIndexData(connection):
    query = "SELECT h.SongId, HIndex, Year FROM lyrics.HIndex h inner join lyrics.songs s on h.SongId = s.SongId;"
    df = pd.read_sql(query, connection)
    connection.close()
    return df

def GetStemmedHIndexData(connection):
    query = "SELECT h.SongId, HIndex, Year FROM lyrics.StemmedHIndex h inner join lyrics.songs s on h.SongId = s.SongId;"
    df = pd.read_sql(query, connection)
    connection.close()
    return df

def GetStemmedMetroHIndexData(connection):
    query = "SELECT h.MetroLyricId, HIndex, Year FROM lyrics.StemmedMetroLyricHIndex h inner join lyrics.MetroLyrics m on h.MetroLyricId = m.MetroLyricId;"
    df = pd.read_sql(query, connection)
    connection.close()
    return df

def GetMetroHIndexData(connection):
    query = "SELECT h.MetroLyricId, HIndex, Year FROM lyrics.MetroLyricHIndex h inner join lyrics.MetroLyrics m on h.MetroLyricId = m.MetroLyricId;"
    df = pd.read_sql(query, connection)
    connection.close()
    return df

def GetComplexityIndex(connection):
       query = "select * from lyrics.ComplexityIndex"
       df = pd.read_sql(query, connection)
       connection.close()
       return df

def UpdateStemmedLyrics(lyrics, songId, connection):
    with connection.cursor() as cursor:
           sql = "UPDATE metrolyrics SET StemmedLyrics = %s WHERE MetroLyricId = %s "
           cursor.execute(sql, (str(lyrics),str(songId)))
           connection.commit()
    cursor.close();

def InsertRepIndex(repIndex, connection):
    with connection.cursor() as cursor:
       for i in range(len(repIndex)):
           sql = "INSERT INTO RepIndex (SongId,Token,Count) VALUES (%s,%s,%s) "
           cursor.execute(sql, (str(repIndex[i][0]),str(repIndex[i][1]), str(repIndex[i][2])))
           connection.commit()
    cursor.close();


def InsertComplexityIndex(connection):
    with connection.cursor() as cursor:
        sql = "INSERT INTO ComplexityIndex (SongId,SentenceCount,WordCount,AvgSyllablesPerWord,AvgSentenceLength,DifficultWordCount,SyllableCount,GunningFog,PolySyllable,SmogIndex,DaleChall,Flesch) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        cursor.execute(sql, (songid,sc,wc,spw,sl,dw,s,g,plsy,si,d,fl))
        connection.commit()
        cursor.close();