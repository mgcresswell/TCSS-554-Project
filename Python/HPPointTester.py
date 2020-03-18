import numpy as np
import pymysql
import pymysql.cursors
import pandas as pd
import DbFunctions as db
from scholarmetrics import hindex

def Tokenize(s):
    tokens = []
    for w in s.split():
        tokens.append(w)
    return tokens

def hIndex2(citations):
        n = len(citations)
        equal_h = [0] * (n+1)
        for h in range(n):
            if citations[h] >= n: equal_h[n] += 1
            else: equal_h[citations[h]] += 1     
        s = 0
        for h in range(n,0, -1):
            s += equal_h[h]
            if s>=h:
                return h          
        return 0

def GroupTokens(tokens):
    repIndex = []
    df = pd.DataFrame(data=tokens, columns=['tokens'])
    gk = df.groupby('tokens').size().to_frame('size')
    gk = gk.reset_index()
    sgk = gk.sort_values(by='size', ascending=False)
    return np.array(sgk['size'])




s = "ah ha ha ha ha ha ha ha ha ha ha ha wipe out"
tokens = Tokenize(s)
gr = GroupTokens(tokens)
h1 = hindex(gr)
h2 = hIndex2(gr)
