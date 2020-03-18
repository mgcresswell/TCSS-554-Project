using HtmlAgilityPack;
using LyricsLibrary;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace LyricsCrawler
{
    public class GeniusAPI
    {
        public static void GetHtml(int i)
        {
            var builder = new StringBuilder();
            try
            {
                HttpWebRequest request = (HttpWebRequest)WebRequest.Create($"https://api.genius.com/songs/{i}?access_token=rSyQKOTKyiFVo1aKDU4k15fPlWTHvt8GSLgDhOOqZ2zb-0nCGpYintiNxm402qxL");
                var jar = new CookieContainer();
                jar.Add(new Cookie("user_credentials", "1065b200883e1c29a225f6f6b4de3e2526bb32e6aef494a18c12698c8326f62f61b7612c9755c869a77c9a28619bef6382abfa4dca3e80f34147adce02729094", "/", ".genius.com"));
                //jar.Add(new Cookie("user-agent", "https://github.com/johnwmillr/LyricsGenius", "/", ".genius.com"));
                //jar.Add(new Cookie("authorization", "Bearer I4eJxKRtO54IdAYsekpsguDkEsR_uHhgULzNCGQvBUTr_8sGxCb_z79giG9epdbk", "/", ".genius.com"));

                request.CookieContainer = jar;
                HttpWebResponse response = (HttpWebResponse)request.GetResponse();
                if (response.StatusCode == HttpStatusCode.OK)
                {
                    Stream receiveStream = response.GetResponseStream();
                    StreamReader readStream = null;

                    if (response.CharacterSet == null)
                    {
                        readStream = new StreamReader(receiveStream);
                    }
                    else
                    {
                        readStream = new StreamReader(receiveStream, Encoding.GetEncoding(response.CharacterSet));
                    }

                    string data = readStream.ReadToEnd();
                    response.Close();
                    readStream.Close();
                    var json = JObject.Parse(data);
                    var date = json.SelectToken("response.song.release_date").Value<string>();
                    if (!string.IsNullOrEmpty(date))
                    {
                        var artist = json.SelectToken("response.song.album.artist.name").Value<string>();
                        var fullTitle = json.SelectToken("response.song.full_title").Value<string>();
                        var url = json.SelectToken("response.song.url").Value<string>();
                        var lyrics = GetLyrics(url);
                        if (!string.IsNullOrEmpty(lyrics))
                        {
                            var splits = new string[] { "by" };
                            var songTitle = fullTitle.Split(splits, StringSplitOptions.None).ElementAt(0).Trim();
                            var lastFm = GetTags(artist, songTitle);
                            if (lastFm.tags.Any())
                            {
                                var genreSong = new GenreSong
                                {
                                    artist = artist.Replace("'", "").Replace("\"", ""),
                                    lyrics = lyrics,
                                    songId = i,
                                    name = songTitle.Replace("'", "").Replace("\"", ""),
                                    date = date
                                };
                                GenreSong.InsertGenreSong(genreSong, lastFm);
                            }
                        }
                       
                    }
                }
                else
                {
                    Console.WriteLine($"{i} Failed");
                }
            }
            catch (Exception e)
            {
                Console.WriteLine($"{i} Failed");
            }
        }

        public static string GetLyrics(string url)
        {
            try
            {
                HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
                HttpWebResponse response = (HttpWebResponse)request.GetResponse();
                if (response.StatusCode == HttpStatusCode.OK)
                {
                    Stream receiveStream = response.GetResponseStream();
                    StreamReader readStream = null;

                    if (response.CharacterSet == null)
                    {
                        readStream = new StreamReader(receiveStream);
                    }
                    else
                    {
                        readStream = new StreamReader(receiveStream, Encoding.GetEncoding(response.CharacterSet));
                    }

                    string data = readStream.ReadToEnd();
                    response.Close();
                    readStream.Close();
                    var doc = new HtmlDocument();
                    doc.LoadHtml(data);
                    var lyrics = doc.DocumentNode.SelectSingleNode("//div[@class='lyrics']").InnerText.Trim().ToLower();
                    lyrics = lyrics.ToString().Replace("'", "");
                    lyrics = lyrics.ToString().Replace("\"", "");
                    return lyrics;
                }
                else
                {
                }
            }
            catch (Exception e)
            {
                return string.Empty;
            }
            return string.Empty;
        }


        public static LastFmModel GetTags(string artist, string track)
        {
            var model = new LastFmModel();
            try
            {
                var URL = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=40c94002d54ba7f37fcef78792bf55ce&artist=" + artist + "&track=" + track + "&format=json";
                var w = new WebClient();
                var json = JObject.Parse(w.DownloadString(URL));
                model.Artist = json.SelectToken("track.artist.name").Value<string>().Replace("'", "").Replace("\"", "");
                model.Title = json.SelectToken("track.name").Value<string>().Replace("'", "").Replace("\"", "");
                model.Duration = json.SelectToken("track.duration").Value<string>();
                model.Playcount = json.SelectToken("track.playcount").Value<string>();
                model.Listeners = json.SelectToken("track.listeners").Value<string>();
                foreach (var tag in json.SelectToken("track.toptags.tag").ToList())
                {
                    model.tags.Add(tag.SelectToken("name").Value<string>());
                }
            }
            catch (Exception e)
            {
                return new LastFmModel();
            }
            return model;
        }
    }

}
    
