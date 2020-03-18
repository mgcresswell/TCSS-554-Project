using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LyricsLibrary
{
    public class LastFmModel
    {
        public string Artist { get; set; }
        public string Title { get; set; }
        public string Duration { get; set; }
        public string Playcount { get; set; }
        public string Listeners { get; set; }

        public List<string> tags = new List<string>();
    }
}
