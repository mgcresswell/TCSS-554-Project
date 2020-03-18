using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LyricsLibrary
{
    public class GeniusSong
    {
        public int songId { get; set; }
        public string name { get; set; }
        public string artist { get; set; }
        public string geniusName { get; set; }
        public string geniusArtist { get; set; }
        public string lyrics { get; set; }

        public static bool InsertCrawledLyrics(Song song)
        {
            var MyConString = "SERVER=35.233.229.223;DATABASE=lyrics;UID=cressm;PASSWORD=Welcome1234!;";
            using (MySqlConnection connection = new MySqlConnection(MyConString))
            {
                try
                {
                    string cmdText = $"UPDATE GeniusSongs SET CrawledLyrics = '{song.lyrics}' WHERE SongId = {song.songId}";
                    MySqlCommand cmd = new MySqlCommand(cmdText, connection);
                    connection.Open();
                    int result = cmd.ExecuteNonQuery();
                }
                catch (Exception e)
                {
                    e.ToString();
                    return false;
                }
            }
            return true;
        }

        public static List<GeniusSong> ReadSongs(string where = null)
        {
            var songs = new List<GeniusSong>();
            var cs = "SERVER=35.233.229.223;DATABASE=lyrics;UID=cressm;PASSWORD=Welcome1234!;";
            using (var con = new MySqlConnection(cs))
            {
                con.Open();
                string sql = "SELECT SongId, Name, Artist, GeniusSongName, GeniusArtist, Lyrics FROM GeniusSongs " + where;
                using (var cmd = new MySqlCommand(sql, con))
                {
                    using (MySqlDataReader rdr = cmd.ExecuteReader())
                    {
                        while (rdr.Read())
                        {
                            var newSong = new GeniusSong();
                            newSong.songId = rdr.GetInt32(0);
                            newSong.name = rdr.IsDBNull(1) ? null : rdr.GetString(1);
                            newSong.artist = rdr.IsDBNull(2) ? null : rdr.GetString(2);
                            newSong.geniusName = rdr.IsDBNull(3) ? null : rdr.GetString(3);
                            newSong.geniusArtist = rdr.IsDBNull(4) ? null : rdr.GetString(4);
                            newSong.lyrics = rdr.IsDBNull(5) ? null : rdr.GetString(5);
                            songs.Add(newSong);
                        }
                    }
                }
            }
            return songs;
        }
    }
}
