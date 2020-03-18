import scipy.stats as stats
from scipy.stats import spearmanr
import pymysql
import pymysql.cursors
import spacy 
import pandas as pd
import DbFunctions as db
from textstat.textstat import textstatistics, easy_word_set, legacy_round 
from scipy.stats import kendalltau
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import (pairwise_tukeyhsd, MultiComparison)




def getSpearman(x,y):
    coef, p = spearmanr(x, y)
    print('Spearmans correlation coefficient: %.10f' % coef)
    alpha = 0.05
    if p > alpha:
        print('Samples are uncorrelated (fail to reject H0) p=%.10f' % p)
    else:
        print('Samples are correlated (reject H0) p=%.10f' % p)


def getKendall(x,y):
    coef, p = kendalltau(x, y)
    print('Kendall correlation coefficient: %.10f' % coef)
    alpha = 0.05
    if p > alpha:
        print('Samples are uncorrelated (fail to reject H0) p=%.10f' % p)
    else:
        print('Samples are correlated (reject H0) p=%.10f' % p)


connection = db.GetCloudConnection()
query = "SELECT c.*, s.Year FROM lyrics.ComplexityIndex c inner join lyrics.songs s on s.SongId = c.SongId; "
songsDf = pd.read_sql(query, connection)

metricDf = songsDf[['SentenceCount','WordCount','AvgSyllablesPerWord','AvgSentenceLength','DifficultWordCount','SyllableCount','GunningFog','PolySyllable','SmogIndex','DaleChall','Flesch','Year']]
averageDf = metricDf.groupby("Year").mean()
x = averageDf.index.values
WordCount = averageDf[['WordCount']].to_numpy().ravel() 
AvgSyllablesPerWord = averageDf[['AvgSyllablesPerWord']].to_numpy().ravel() 
GunningFog = averageDf[['GunningFog']].to_numpy().ravel() 
SmogIndex = averageDf[['SmogIndex']].to_numpy().ravel() 
DaleChall = averageDf[['DaleChall']].to_numpy().ravel() 
Flesch = averageDf[['Flesch']].to_numpy().ravel() 

print("Billboard Word Count")
getKendall(x, WordCount)
getSpearman(x, WordCount)

print("Billboard Avergae Syllable Per Word")
getKendall(x, AvgSyllablesPerWord)
getSpearman(x, AvgSyllablesPerWord)

print("Billboard Gunning Fog")
getKendall(x, GunningFog)
getSpearman(x, GunningFog)

print("Billboard Smog Index")
getKendall(x, SmogIndex)
getSpearman(x, SmogIndex)

print("Billboard Dale Chall")
getKendall(x, DaleChall)
getSpearman(x, DaleChall)

print("Billboard Flesch")
getKendall(x, Flesch)
getSpearman(x, Flesch)

#Gunning Fog
#genres = ['Country','Electronic','Folk','Hip-Hop','Indie','Jazz','Metal','Pop','R&B','Rock']
#connection = db.GetCloudConnection()
#HIndex = pd.DataFrame(data=None, columns=genres)
#for i in range(len(genres)):
#    genreQuery = "select GunningFog, Genre from MetroLyrics m inner join MetroLyricsComplexityIndex c on m.MetroLyricId = c.SongId"
#    HIndex[genres[i]] = pd.Series(pd.read_sql(genreQuery, connection).to_numpy().ravel())

#d_melt = pd.melt(HIndex.reset_index(), id_vars=['index'], value_vars=['Country','Electronic','Folk','Hip-Hop','Indie','Jazz','Metal','Pop','R&B','Rock'])
#d_melt.columns = ['index', 'genre', 'value']
#model = ols('value ~ C(genre)', data=d_melt).fit()
#anova_table = sm.stats.anova_lm(model, typ=2)
#print(anova_table)
#m_comp = pairwise_tukeyhsd(endog=d_melt['value'], groups=d_melt['genre'], alpha=0.05)
#print(m_comp)

connection = db.GetCloudConnection()
genreQuery = "select GunningFog, Genre from MetroLyrics m inner join MetroLyricsComplexityIndex c on m.MetroLyricId = c.SongId"
songsDf = pd.read_sql(genreQuery, connection)

mod = MultiComparison(songsDf['GunningFog'], songsDf['Genre'])
print(mod.allpairtest(stats.ttest_ind, method='b')[0])

#SmogIndex
#connection = db.GetCloudConnection()
#HIndex = pd.DataFrame(data=None, columns=genres)
#for i in range(len(genres)):
#    genreQuery = "select SmogIndex from MetroLyrics m inner join MetroLyricsComplexityIndex c on m.MetroLyricId = c.SongId WHERE Genre = '" + genres[i] +"'"
#    HIndex[genres[i]] = pd.Series(pd.read_sql(genreQuery, connection).to_numpy().ravel())

#d_melt = pd.melt(HIndex.reset_index(), id_vars=['index'], value_vars=['Country','Electronic','Folk','Hip-Hop','Indie','Jazz','Metal','Pop','R&B','Rock'])
#d_melt.columns = ['index', 'genre', 'value']
#model = ols('value ~ C(genre)', data=d_melt).fit()
#anova_table = sm.stats.anova_lm(model, typ=2)
#print(anova_table)
#m_comp = pairwise_tukeyhsd(endog=d_melt['value'], groups=d_melt['genre'], alpha=0.05)
#print(m_comp)

connection = db.GetCloudConnection()
genreQuery = "select SmogIndex, Genre from MetroLyrics m inner join MetroLyricsComplexityIndex c on m.MetroLyricId = c.SongId"
songsDf = pd.read_sql(genreQuery, connection)

mod = MultiComparison(songsDf['SmogIndex'], songsDf['Genre'])
print(mod.allpairtest(stats.ttest_ind, method='b')[0])

#DaleChall
#HIndex = pd.DataFrame(data=None, columns=genres)
#for i in range(len(genres)):
#    genreQuery = "select DaleChall from MetroLyrics m inner join MetroLyricsComplexityIndex c on m.MetroLyricId = c.SongId WHERE Genre = '" + genres[i] +"'"
#    HIndex[genres[i]] = pd.Series(pd.read_sql(genreQuery, connection).to_numpy().ravel())

#d_melt = pd.melt(HIndex.reset_index(), id_vars=['index'], value_vars=['Country','Electronic','Folk','Hip-Hop','Indie','Jazz','Metal','Pop','R&B','Rock'])
#d_melt.columns = ['index', 'genre', 'value']
#model = ols('value ~ C(genre)', data=d_melt).fit()
#anova_table = sm.stats.anova_lm(model, typ=2)
#print(anova_table)
#m_comp = pairwise_tukeyhsd(endog=d_melt['value'], groups=d_melt['genre'], alpha=0.05)
#print(m_comp)

connection = db.GetCloudConnection()
genreQuery = "select DaleChall, Genre from MetroLyrics m inner join MetroLyricsComplexityIndex c on m.MetroLyricId = c.SongId"
songsDf = pd.read_sql(genreQuery, connection)

mod = MultiComparison(songsDf['DaleChall'], songsDf['Genre'])
print(mod.allpairtest(stats.ttest_ind, method='b')[0])

#Flesch
#HIndex = pd.DataFrame(data=None, columns=genres)
#for i in range(len(genres)):
#    genreQuery = "select Flesch from MetroLyrics m inner join MetroLyricsComplexityIndex c on m.MetroLyricId = c.SongId WHERE Genre = '" + genres[i] +"'"
#    HIndex[genres[i]] = pd.Series(pd.read_sql(genreQuery, connection).to_numpy().ravel())

#d_melt = pd.melt(HIndex.reset_index(), id_vars=['index'], value_vars=['Country','Electronic','Folk','Hip-Hop','Indie','Jazz','Metal','Pop','R&B','Rock'])
#d_melt.columns = ['index', 'genre', 'value']
#model = ols('value ~ C(genre)', data=d_melt).fit()
#anova_table = sm.stats.anova_lm(model, typ=2)
#print(anova_table)
#m_comp = pairwise_tukeyhsd(endog=d_melt['value'], groups=d_melt['genre'], alpha=0.05)
#print(m_comp)

connection = db.GetCloudConnection()
genreQuery = "select Flesch, Genre from MetroLyrics m inner join MetroLyricsComplexityIndex c on m.MetroLyricId = c.SongId"
songsDf = pd.read_sql(genreQuery, connection)

mod = MultiComparison(songsDf['Flesch'], songsDf['Genre'])
print(mod.allpairtest(stats.ttest_ind, method='b')[0])