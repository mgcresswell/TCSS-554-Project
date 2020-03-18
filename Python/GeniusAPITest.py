import sys
sys.path.append('C:\\Users\\cressm\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages')

import lyricsgenius
import pymysql;
import pandas as pd;
import requests;
import RadioFmAPI as fm;
import DbFunctions as db


genius = lyricsgenius.Genius("I4eJxKRtO54IdAYsekpsguDkEsR_uHhgULzNCGQvBUTr_8sGxCb_z79giG9epdbk")
genius.verbose = False # Turn off status messages
genius.remove_section_headers = True # Remove section headers (e.g. [Chorus]) from lyrics when searching
genius.skip_non_songs = True # Include hits thought to be non-songs (e.g. track lists)
genius.excluded_terms = ["(Remix)", "(Live)"] # Exclude songs with these words in their title
genius.timeout = 30

newconnection = db.GetCloudConnection()

count = 60369
while (count < 1000000): 
    try:
        song = genius.get_song(count)  
        if song != None:
            artist = song['song']['album']['artist']['name']
            fullTitle = song['song']['full_title']
            date = song['song']['release_date']
            if date != None :
                songTitle = fullTitle.split('by')[0]
                songTitle = songTitle.strip()
                songSearch = genius.search_song(songTitle, artist = artist)
                fmsong = fm.GetSongInfo(artist,songTitle)
                   
                if fmsong != None:
                    if len(fmsong.tags) > 0:                     
                        with newconnection.cursor() as cursor:
                           sql = "INSERT INTO GenreSongs (GenreSongId, LastfmTitle, LastfmArtist, Date, GeniusSongId, GeniusArtist, GeniusTitle, Duration, PlayCount, Listeners, Lyrics) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                           cursor.execute(sql, (str(count), str(fmsong.title),str(fmsong.artist), str(date), str(count), str(artist), str(songTitle), str(fmsong.duration), str(fmsong.playcount), str(fmsong.listeners), str(songSearch.lyrics)))
                           newconnection.commit()
                        cursor.close();

                        with newconnection.cursor() as cursor2:
                           for i in range(len(fmsong.tags)):
                            sql = "INSERT INTO GenreSongTags (GenreSongId, Tag) VALUES (%s,%s) "
                            cursor2.execute(sql, (str(count), str(fmsong.tags[i]['name'])))
                            newconnection.commit()
                        cursor.close();
        count = count + 1
    except:
        count = count + 1
        print(str(count) + " Failed")
       





   
    

       
