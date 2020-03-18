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
    print('Spearmans correlation coefficient: %.3f' % coef)
    alpha = 0.05
    if p > alpha:
        print('Samples are uncorrelated (fail to reject H0) p=%.3f' % p)
    else:
        print('Samples are correlated (reject H0) p=%.3f' % p)


def getKendall(x,y):
    coef, p = kendalltau(x, y)
    print('Kendall correlation coefficient: %.3f' % coef)
    alpha = 0.05
    if p > alpha:
        print('Samples are uncorrelated (fail to reject H0) p=%.3f' % p)
    else:
        print('Samples are correlated (reject H0) p=%.3f' % p)

#StemmedRepIndex Correlation
connection = db.GetCloudConnection()
repIndex = db.GetStemmedRepIndex(connection)
totalsDf = repIndex.groupby('SongId').agg({'Count': ['sum']}).reset_index()
filteredRepIndex = repIndex[repIndex['Count'] > 1]
filterdDf = filteredRepIndex.groupby('SongId').agg({'Count': ['sum']}).reset_index()
metric = []
for index, row in totalsDf.iterrows(): 
    countRow = filterdDf[filterdDf['SongId'] == row[0]]
    countRow = countRow.to_numpy().ravel() 
    if len(countRow) > 0:
        year = repIndex[repIndex['SongId'] == row[0]]
        year = year.to_numpy().ravel()    
        metric.append([countRow[0],year[1],countRow[1]/row[1]])

metricDf = pd.DataFrame(data=metric, columns=['SongId','Year','Metric'])
gr = metricDf.groupby('Year').agg({'Metric': ['mean']}).reset_index()
x = gr[['Year']].to_numpy().ravel() 
y = gr[['Metric']].to_numpy().ravel() 
getKendall(x, y)
getSpearman(x, y)

#RepIndex Correlation
connection = db.GetCloudConnection()
repIndex = db.GetRepIndex(connection)
totalsDf = repIndex.groupby('SongId').agg({'Count': ['sum']}).reset_index()
filteredRepIndex = repIndex[repIndex['Count'] > 1]
filterdDf = filteredRepIndex.groupby('SongId').agg({'Count': ['sum']}).reset_index()
metric = []
for index, row in totalsDf.iterrows(): 
    countRow = filterdDf[filterdDf['SongId'] == row[0]]
    countRow = countRow.to_numpy().ravel() 
    if len(countRow) > 0:
        year = repIndex[repIndex['SongId'] == row[0]]
        year = year.to_numpy().ravel()    
        metric.append([countRow[0],year[1],countRow[1]/row[1]])

metricDf = pd.DataFrame(data=metric, columns=['SongId','Year','Metric'])
gr = metricDf.groupby('Year').agg({'Metric': ['mean']}).reset_index()
x = gr[['Year']].to_numpy().ravel() 
y = gr[['Metric']].to_numpy().ravel() 
getKendall(x, y)
getSpearman(x, y)

#HIndex Correlation
connection = db.GetCloudConnection()
songs = db.GetHIndexData(connection)
gr = songs.groupby('Year').agg({'HIndex': ['mean']}).reset_index()
x = gr[['Year']].to_numpy().ravel() 
y = gr[['HIndex']].to_numpy().ravel() 
getKendall(x, y)
getSpearman(x, y)

#StemmedHIndex Correlation
connection = db.GetCloudConnection()
songs = db.GetStemmedHIndexData(connection)
gr = songs.groupby('Year').agg({'HIndex': ['mean']}).reset_index()
x = gr[['Year']].to_numpy().ravel() 
y = gr[['HIndex']].to_numpy().ravel() 
getKendall(x, y)
getSpearman(x, y)

#Metro StemmedHIndex Correlation
connection = db.GetCloudConnection()
songs = db.GetStemmedMetroHIndexData(connection)
gr = songs.groupby('Year').agg({'HIndex': ['mean']}).reset_index()
x = gr[['Year']].to_numpy().ravel() 
y = gr[['HIndex']].to_numpy().ravel() 
getKendall(x, y)
getSpearman(x, y)

#Metro HIndex Correlation
#connection = db.GetCloudConnection()
#songs = db.GetMetroHIndexData(connection)
#gr = songs.groupby('Year').agg({'HIndex': ['mean']}).reset_index()
#x = gr[['Year']].to_numpy().ravel() 
#y = gr[['HIndex']].to_numpy().ravel() 
#getKendall(x, y)
#getSpearman(x, y)





connection = db.GetCloudConnection()
HIndex = pd.DataFrame(data=None, columns=['HIndex','Genre'])
#for i in range(len(genres)):
genreQuery = "select HIndex, Genre from MetroLyrics m inner join MetroLyricHIndex h on m.MetroLyricId = h.MetroLyricId"
songsDf = pd.read_sql(genreQuery, connection)

mod = MultiComparison(songsDf['HIndex'], songsDf['Genre'])
print(mod.allpairtest(stats.ttest_ind, method='b')[0])

#d_melt = pd.melt(HIndex.reset_index(), id_vars=['index'], value_vars=['Country','Electronic','Folk','Hip-Hop','Indie','Jazz','Metal','Pop','R&B','Rock'])
#d_melt.columns = ['index', 'genre', 'value']
#model = ols('value ~ C(genre)', data=d_melt).fit()
#anova_table = sm.stats.anova_lm(model, typ=2)
#print(anova_table)

#m_comp = pairwise_tukeyhsd(endog=d_melt['value'], groups=d_melt['genre'], alpha=0.05)
#print(m_comp)





