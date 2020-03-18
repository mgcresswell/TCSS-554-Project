
import lyricsgenius
import pymysql;
import pandas as pd;

#genius = lyricsgenius.Genius("I4eJxKRtO54IdAYsekpsguDkEsR_uHhgULzNCGQvBUTr_8sGxCb_z79giG9epdbk")
#genius.verbose = False # Turn off status messages
#genius.remove_section_headers = True # Remove section headers (e.g. [Chorus]) from lyrics when searching
#genius.skip_non_songs = False # Include hits thought to be non-songs (e.g. track lists)
#genius.excluded_terms = ["(Remix)", "(Live)"] # Exclude songs with these words in their title
#genius.timeout = 30;

connection = pymysql.connect(host='35.233.229.223',
                             user='cressm',
                             password='Welcome1234!',
                             db='lyrics',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

query = "select * from lyrics.songs"
songs = pd.read_sql(query, connection)

query2 = "select * from lyrics.GeniusSongs"
geniusSongs = pd.read_sql(query2, connection)
connection.close()


newconnection = pymysql.connect(host='35.233.229.223',
                                 user='cressm',
                                 password='Welcome1234!',
                                 db='lyrics',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
dups = []
for index, row in geniusSongs.iterrows(): 
    
            filter = (songs["Name"] == row["Name"]) & (songs["Artist"] == row["Artist"]) & (songs["Year"] == row["Year"])
            songRecord = songs[filter]

            songRecord = songRecord.iloc[ 0 , : ] 

            newconnection = pymysql.connect(host='35.233.229.223',
                                 user='cressm',
                                 password='Welcome1234!',
                                 db='lyrics',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
            

            cursor = newconnection.cursor()
            sql = "UPDATE lyrics.GeniusSongs SET SongId = '"+ str(songRecord["SongId"]) +"'  WHERE Id = '"+ str(row["Id"]) +"';"
            cursor.execute(sql)            
            newconnection.commit();
            cursor.close()
            newconnection.close()
        

            newconnection2 = pymysql.connect(host='35.233.229.223',
                                 user='cressm',
                                 password='Welcome1234!',
                                 db='lyrics',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

            lyrics = row["Lyrics"].replace('\'', '')
            cursor2 = newconnection2.cursor()
            sql2 = "UPDATE lyrics.songs SET GeniusLyrics ='"+ lyrics +"' WHERE SongId = '"+ str(songRecord["SongId"]) +"';"
            cursor2.execute(sql2)            
            newconnection2.commit();
            cursor.close()
            newconnection2.close()         


t = 1
    
       