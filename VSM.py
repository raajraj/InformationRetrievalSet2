#!/usr/bin/python

import sys
import parsing
import array
import math
from operator import itemgetter
from dataclasses import dataclass
from decimal import Decimal
import re
import os
import zipfile

docSize = parsing.getDocSize()
querylist = sys.argv[1]
class qtoken: # query token class
    term = ""
    termFrequency = 0
    queryNumber = 0
    TF = [] # TF list
    DF = 0 # DF
    TFIDF = [] # TFIDF list
    qTFIDF = 0; # query TFIDF

# start pulling from query list
with open(querylist) as f:
    for line in f: # for a single query
        qcosSim = list()
        query = set() # set of words
        qNum = 0 # query number
        wordFrequency = list()
        queryList = list() # list of words with repeats
        # split line
        line = line.split()
        # omit the number
        if(len(line) > 1):
            qNum = line[0]
            del line[0]
        
        punc = '''!()-[]{};:'"``\, <>./?@#$%^&*_~''' # punctuation to remove
        numbers_and_letters = "1234567890abcdefghijklmnopqrstuvwxyz"
            
        for word in line: # for all the words in the query
            currWordFreq = 0
            word = word.lower() # lower case the word
            # remove punctuation
            x = 0
            for ele in word:
                if ele in punc:
                    if((x > 0) & (x < len(word) - 1) & (ele == '.')):
                        if((word[x - 1] not in numbers_and_letters) | (word[x + 1] not in numbers_and_letters)):
                            word = word.replace(ele, "")
                        else:
                            continue
                    else:
                        word = word.replace(ele, "")
                    if(x == len(word) - 1):
                        word = word.replace(ele, "")
                x = x + 1
            if(parsing.not_stopWord(word)):
                queryList.append(word) # add to list
                currqt = qtoken()
                currqt.term = word
                currqt.queryNumber = qNum
                query.add(currqt) # add to set
        
        for w in query: # for all the words in the set
            w.TF = parsing.getTF(w.term) # get TF list for word
            w.DF = parsing.getDF(w.term) # get DF for word
            for x in w.TF:
                w.TFIDF.append(float(x)*w.DF) # list of TFIDF
            for t in queryList:
                if(w.term == t):
                    w.termFrequency = (w.termFrequency + 1)/(float(len(queryList))) # get term frequency for query
                    w.qTFIDF = w.DF*w.termFrequency # TFIDF for query
        num = 0
        denom1 = 0
        denom2 = 0
        # now we find the cosine similarity
        for docs in range(docSize): # for each document
            for term in query: # grab cos similarity
                num = num + term.TFIDF[docs] * term.qTFIDF
                denom1 = denom1 + term.TFIDF[docs]**2
                denom2 = denom2 + term.qTFIDF**2
            if((denom1*denom2) != 0):
                cos_sim = num/(math.sqrt(denom1*denom2))
            else:
                cos_sim = 0
            qcosSim.append((cos_sim, docs+1))
        
        def sortFirst(val):
            return val[0]
        
        qcosSim.sort(key = sortFirst, reverse = True)
        
        rank = 1
        for output in qcosSim:
            if(rank <= 10):
                docno = parsing.findDocNum(output[1])
                print(qNum + " Q0 " + docno + " " + "%2d"%rank + " " + "{:.5f}".format(output[0]) + " Exp")
                rank = rank  + 1
