import pymysql
import pymysql.cursors
import spacy 
import pandas as pd
import DbFunctions as db
from textstat.textstat import textstatistics, easy_word_set, legacy_round 

# Splits the text into sentences, using  
# Spacy's sentence segmentation which can  
# be found at https://spacy.io/usage/spacy-101 
def break_sentences(text): 
    nlp = nlp = spacy.load("C:\\Users\\cressm\\AppData\\Local\\Continuum\\anaconda3\\envs\\NewEnviroment\\Lib\\site-packages\\en_core_web_sm\\en_core_web_sm-2.2.0")
    doc = nlp(text) 
    return doc.sents 

# Returns Number of Words in the text 
def word_count(text): 
    sentences = break_sentences(text) 
    words = 0
    for sentence in sentences: 
        words += len([token for token in sentence]) 
    return words 
  
# Returns the number of sentences in the text 
def sentence_count(text): 
    sentences = break_sentences(text) 
    i = 0;
    for sentence in sentences: 
        i = i + 1
    return i
  
# Returns average sentence length 
def avg_sentence_length(text): 
    words = word_count(text) 
    sentences = sentence_count(text) 
    average_sentence_length = float(words / sentences) 
    return average_sentence_length 
  
# Textstat is a python package, to calculate statistics from  
# text to determine readability,  
# complexity and grade level of a particular corpus. 
# Package can be found at https://pypi.python.org/pypi/textstat 
def syllables_count(word): 
    return textstatistics().syllable_count(word) 
  
# Returns the average number of syllables per 
# word in the text 
def avg_syllables_per_word(text): 
    syllable = syllables_count(text) 
    words = word_count(text) 
    ASPW = float(syllable) / float(words) 
    return legacy_round(ASPW, 10) 
  
# Return total Difficult Words in a text 
def difficult_words(text): 
  
    # Find all words in the text 
    words = [] 
    sentences = break_sentences(text) 
    for sentence in sentences: 
        words += [str(token) for token in sentence] 
  
    # difficult words are those with syllables >= 2 
    # easy_word_set is provide by Textstat as  
    # a list of common words 
    diff_words_set = set() 
      
    for word in words: 
        syllable_count = syllables_count(word) 
        if word not in easy_word_set and syllable_count >= 2: 
            diff_words_set.add(word) 
  
    return len(diff_words_set) 
  
# A word is polysyllablic if it has more than 3 syllables 
# this functions returns the number of all such words  
# present in the text 
def poly_syllable_count(text): 
    count = 0
    words = [] 
    sentences = break_sentences(text) 
    for sentence in sentences: 
        words += [str(token) for token in sentence] 
      
  
    for word in words: 
        syllable_count = syllables_count(word) 
        if syllable_count >= 3: 
            count += 1
    return count 
  
  
def flesch_reading_ease(text): 
    """ 
        Implements Flesch Formula: 
        Reading Ease score = 206.835 - (1.015 × ASL) - (84.6 × ASW) 
        Here, 
          ASL = average sentence length (number of words  
                divided by number of sentences) 
          ASW = average word length in syllables (number of syllables  
                divided by number of words) 
    """
    FRE = 206.835 - float(1.015 * avg_sentence_length(text)) - float(84.6 * avg_syllables_per_word(text)) 
    return legacy_round(FRE, 10) 
  
  
def gunning_fog(text): 
    per_diff_words = (difficult_words(text) / word_count(text) * 100) + 5
    grade = 0.4 * (avg_sentence_length(text) + per_diff_words) 
    return grade 
  
  
def smog_index(text): 
    """ 
        Implements SMOG Formula / Grading 
        SMOG grading = 3 + ?polysyllable count. 
        Here,  
           polysyllable count = number of words of more 
          than two syllables in a sample of 30 sentences. 
    """
  
    if sentence_count(text) >= 3: 
        poly_syllab = poly_syllable_count(text) 
        SMOG = (1.043 * (30*(poly_syllab / sentence_count(text)))**0.5) + 3.1291
        return legacy_round(SMOG, 10) 
    else: 
        return 0
  
  
def dale_chall_readability_score(text): 
    """ 
        Implements Dale Challe Formula: 
        Raw score = 0.1579*(PDW) + 0.0496*(ASL) + 3.6365 
        Here, 
            PDW = Percentage of difficult words. 
            ASL = Average sentence length 
    """
    words = word_count(text) 
    # Number of words not termed as difficult words 
    count = words - difficult_words(text) 
    if words > 0: 
        # Percentage of words not on difficult word list 
        per = float(count) / float(words) * 100
      
    # diff_words stores percentage of difficult words 
    diff_words = 100 - per 
    raw_score = (0.1579 * diff_words) + (0.0496 * avg_sentence_length(text)) 
      
    # If Percentage of Difficult Words is greater than 5 %, then; 
    # Adjusted Score = Raw Score + 3.6365, 
    # otherwise Adjusted Score = Raw Score 
    if diff_words > 5:        
        raw_score += 3.6365        
    return legacy_round(raw_score, 10) 

# Connect to the database
connection = db.GetCloudConnection()

query = "Select SongId, ProcessedLyrics FROM songs where ProcessedLyrics is not null and SongId not in (Select SongId FROM ComplexityIndex)"
df = pd.read_sql(query, connection)


for index, row in df.iterrows(): 

    sentencecount = sentence_count(row['ProcessedLyrics'])
    wordcount = word_count(row['ProcessedLyrics'])
    syllableperWord = avg_syllables_per_word(row['ProcessedLyrics'])
    sentlength = avg_sentence_length(row['ProcessedLyrics'])
    difficultwords = difficult_words(row['ProcessedLyrics'])
    syllables = syllables_count(row['ProcessedLyrics'])
    gunning = gunning_fog(row['ProcessedLyrics'])
    polysyllable = poly_syllable_count(row['ProcessedLyrics'])
    sindex = smog_index(row['ProcessedLyrics'])
    dc = dale_chall_readability_score(row['ProcessedLyrics'])
    flesch = flesch_reading_ease(row['ProcessedLyrics'])

    songid = str(row["SongId"])
    sc = str(sentencecount)
    wc = str(wordcount)
    spw = str(round(syllableperWord,10))
    sl = str(sentlength)
    dw = str(difficultwords)
    s = str(syllables)
    g = str(round(gunning, 10))
    plsy = str(polysyllable)
    si = str(round(sindex, 10))
    d = str(round(dc,10))
    fl = str(round(flesch,10))

    with connection.cursor() as cursor:
       sql = "INSERT INTO ComplexityIndex (SongId,SentenceCount,WordCount,AvgSyllablesPerWord,AvgSentenceLength,DifficultWordCount,SyllableCount,GunningFog,PolySyllable,SmogIndex,DaleChall,Flesch) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "   
       cursor.execute(sql, (songid,sc,wc,spw,sl,dw,s,g,plsy,si,d,fl))
       connection.commit()
    cursor.close();
connection.close()