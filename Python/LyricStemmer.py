

from __future__ import print_function
from nltk.stem import *
from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer
import nltk
import os
import __future__
import re 
import numpy
import csv
import pandas as pd
import numpy as np
import math
import DbFunctions as db

def stemmWords(words):
    stemmer = PorterStemmer()
    for x in range(len(words)):
        stemmedWord = stemmer.stem(words[x])
        words[x] = stemmedWord
    return words



connection = db.GetLocalConnection()
songs = db.GetMetroSongs(connection, "where ProcessedLyrics is not null")
processedLyrics = songs[['MetroLyricId','ProcessedLyrics']]
seperator = ' '

for index, row in processedLyrics.iterrows():
    words = []
    songId = row['MetroLyricId']
    lyric = row['ProcessedLyrics']
    for w in lyric.split():
        words.append(w)
    
    stemmedWords = stemmWords(words)
    newLyrics = seperator.join(stemmedWords)
    newconnection = db.GetLocalConnection()
    db.UpdateStemmedLyrics(newLyrics, songId, newconnection)







         