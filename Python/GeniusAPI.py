
import lyricsgenius
import pymysql;
import pandas as pd;



genius = lyricsgenius.Genius("I4eJxKRtO54IdAYsekpsguDkEsR_uHhgULzNCGQvBUTr_8sGxCb_z79giG9epdbk")
genius.verbose = False # Turn off status messages
genius.remove_section_headers = True # Remove section headers (e.g. [Chorus]) from lyrics when searching
genius.skip_non_songs = False # Include hits thought to be non-songs (e.g. track lists)
genius.excluded_terms = ["(Remix)", "(Live)"] # Exclude songs with these words in their title
genius.timeout = 30;

connection = pymysql.connect(host='35.233.229.223',
                             user='cressm',
                             password='Welcome1234!',
                             db='lyrics',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

query = "select * from lyrics.songs where CrawledLyrics is null and name not in (select name from lyrics.GeniusSongs)"
df = pd.read_sql(query, connection)
connection.close()

found = []
notFound = []
for index, row in df.iterrows(): 
    GeniusSongId = 0
    GeniusArtistId = 0
    GeniusSongName = ''
    GeniusArtistName = ''
    Lyrics = ''

    artistResult = genius.search_artist(row["Artist"], max_songs=1, allow_name_change=True)
    if (artistResult != None):
        GeniusArtistName = artistResult.name;
        GeniusArtistId = artistResult._id;
        songResult = genius.search_song(row["Name"], artist = GeniusArtistName)
        if (songResult != None):
            GeniusSongName = songResult.title;
            GeniusSongId = songResult._id;
            Lyrics = songResult.lyrics;
   
    

    newconnection = pymysql.connect(host='35.233.229.223',
                             user='cressm',
                             password='Welcome1234!',
                             db='lyrics',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with newconnection.cursor() as cursor:
        sql = "INSERT INTO GeniusSongs (Name,Artist,Rank,Year,GeniusSongId,GeniusArtistId,Lyrics,GeniusSongName,GeniusArtist) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        cursor.execute(sql, (str(row["Name"]),str(row["Artist"]),str(row["Rank"]),str(row["Year"]),str(GeniusSongId),str(GeniusArtistId),Lyrics,GeniusSongName,GeniusArtistName))
        newconnection.commit()
    cursor.close();
    
       