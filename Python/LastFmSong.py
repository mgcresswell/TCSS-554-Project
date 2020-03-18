class LastFmSong(object):
    artist = ""
    title = ""
    tags = []
    duration = 0
    playcount = 0
    listeners = 0
       
    def __init__(self, artist, title, tags, duration, playcount, listeners):
        self.artist = artist
        self.title = title
        self.tags = tags
        self.duration = duration
        self.playcount = playcount
        self.listeners = listeners
