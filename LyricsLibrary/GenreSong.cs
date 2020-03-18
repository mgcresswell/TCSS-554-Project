using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LyricsLibrary
{
    public class GenreSong
    {
        public int songId { get; set; }
        public string name { get; set; }
        public string artist { get; set; }
        public string lyrics { get; set; }
        public string date { get; set; }

        public static void InsertGenreSong(GenreSong song, LastFmModel lastfm)
        {
            var MyConString = "SERVER=35.233.229.223;DATABASE=lyrics;UID=cressm;PASSWORD=Welcome1234!;";
            using (MySqlConnection connection = new MySqlConnection(MyConString))
            {
                string cmdText = $"INSERT INTO lyrics.GenreSongs VALUES ('{song.songId}','{lastfm.Title}','{lastfm.Artist}','{song.date}','{song.songId}','{song.artist}','{song.name}','{lastfm.Duration}','{lastfm.Playcount}','{lastfm.Listeners}','{song.lyrics}')";
                MySqlCommand cmd = new MySqlCommand(cmdText, connection);
                connection.Open();
                int result = cmd.ExecuteNonQuery();

                foreach (var tag in lastfm.tags)
                {
                    cmdText = $"INSERT INTO lyrics.GenreSongTags (GenreSongId,Tag) VALUES ('{song.songId}','{tag}')";
                    MySqlCommand cmd2 = new MySqlCommand(cmdText, connection);
                    result = cmd2.ExecuteNonQuery();
                }
            }
        }

        public static void InsertSongTag(LastFmModel lastfm, int songId)
        {
            var MyConString = "SERVER=35.233.229.223;DATABASE=lyrics;UID=cressm;PASSWORD=Welcome1234!;";
            using (MySqlConnection connection = new MySqlConnection(MyConString))
            {
                connection.Open();
                foreach (var tag in lastfm.tags)
                {
                    var cmdText = $"INSERT INTO lyrics.songTags (SongId,Tag) VALUES ('{songId}','{tag}')";
                    MySqlCommand cmd2 = new MySqlCommand(cmdText, connection);                  
                    var result = cmd2.ExecuteNonQuery();
                }
            }
        }
    }
}
