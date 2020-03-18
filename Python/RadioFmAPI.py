import requests 
import LastFmSong as fm



def GetSongInfo(artist,track):
        try:
            URL = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=40c94002d54ba7f37fcef78792bf55ce&artist=" + artist + "&track=" + track + "&format=json"
            r = requests.get(url = URL) 
            data = r.json() 
            if not 'message' in data:
                tags = data['track']['toptags']['tag']
                tagList = []
                for x in range(len(tags)):
                    tag = tagList.append(tags[x]['name'])
    
                song = fm.LastFmSong(data['track']['artist']['name'], data['track']['name'], tags, data['track']['duration'], data['track']['playcount'], data['track']['listeners'])
                return song
            else:
                return None
        except: 
            return None

  
GetSongInfo("bob seger", "fire lake")
