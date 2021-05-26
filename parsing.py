#!/usr/bin/python

import re
import os
import zipfile
import array
import math
from operator import itemgetter
from dataclasses import dataclass

class Document: # Document class
    docName = "" # name of doc
    docID = 0 # document ID
    totalTerms = 0 # total number of terms
    distinctTerms = 0 # total number of distinct terms
    
class token: # token class
    term = "" # term name
    termID = 0; # term ID
    frequency = 0 # corpus frequency
    tupleList = list() # list of tuples for term
    docsWithTerm = 0 # number of documents with term
    docFrequency = 0 # requested document frequency
    desiredTuple = (0, 0, 0) # requested tuple
    tfList = [] # list of term frequiencies

# array of stop words
stopWords = ["i", "me" , "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers" ,"herself", "it","its","itself", "they", "them", "their", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with" ,"about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

# initialize tokens
tokens = set()
termNames = set()

# initialize document
documents = set()

# checks whether term is a stop word
def not_stopWord(text):
    for x in stopWords:
        if(text == x):
            return 0
    return 1

# Regular expressions to extract data from the corpus
doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)

with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
    zip_ref.extractall()

# Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory

for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
    allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]

# assign variables
termID = 0
docID = 0
totalTerms = 0
distTerms = 0

# create a set of tokens and documents
for file in allfiles:
    with open(file, 'r', encoding='ISO-8859-1') as f:
        filedata = f.read()
        result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch document

        for document in result[0:]:
            tempDoc = Document() # create a document structure
            
            # set to 0
            totalTerms = 0
            distTerms = 0
            
            # Retrieve contents of DOCNO tag
            docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
            docID = docID + 1 # increment document ID
            tempDoc.docName = docno
            tempDoc.docID = docID
            
            # Retrieve contents of TEXT tag
            text = "".join(re.findall(text_regex, document))\
                          .replace("<TEXT>", "").replace("</TEXT>", "")\
                          .replace("\n", " ")

            text = text.split() # separates words
            punc = '''!()-[]{};:'"``\, <>./?@#$%^&*_~''' # punctuation to remove
            numbers_and_letters = "1234567890abcdefghijklmnopqrstuvwxyz"
            
            for word in text:
                totalTerms = totalTerms + 1 # increment total number of terms
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
                # assign token
                tempWordSet = {word}
                if(not_stopWord(word) & (tempWordSet.isdisjoint(termNames))):
                    distTerms = distTerms + 1
                    termID = termID + 1
                    temp = token()
                    temp.term = word
                    temp.termID = termID
                    tokens.add(temp)
                    termNames.add(word)

            # assign document
            tempDoc.totalTerms = totalTerms
            documents.add(tempDoc)

# This function iterates through the document and tallies statistics

def getIndex(toke, doc):
    docCount = 0 # documents that contain toke
    for sfile in allfiles:
        with open(sfile, 'r', encoding='ISO-8859-1') as f:
            sfiledata = f.read()
            sresult = re.findall(doc_regex, sfiledata)  # Match the <DOC> tags and fetch document
            
            for document in sresult[0:]:
                wordCount = 0
                currF = 0
                termFrequency = 0
                ptuple = (); # position tuple
                position = 0 # position of the token
                
                docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()

                text = "".join(re.findall(text_regex, document))\
                              .replace("<TEXT>", "").replace("</TEXT>", "")\
                              .replace("\n", " ")
                              
                text = text.split()
                punc = '''!()-[]{};:'"``\, <>./?@#$%^&*_~'''
                numbers_and_letters = "1234567890abcdefghijklmnopqrstuvwxyz"
                
                # go through the same motions as before to compare words easily
                for word in text:
                    word = word.lower()
                    
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
                    # check for equality and positions
                    position = position + 1
                    wordCount = wordCount + 1
                    # update total frequency in corpus and position in doc
                    if(toke.term == word):
                        currF = currF + 1
                        toke.frequency = toke.frequency + 1
                        tempTuple = (position, );
                        ptuple = ptuple + tempTuple
                        
                    # if there is a specific document in paramaters, get specific frequency
                    if((doc.docName == docno) & (toke.term == word)):
                        toke.docFrequency = toke.docFrequency + 1
                        
                tuple = (toke.termID, doc.docID, ptuple); #assign tuple
                
                # assign desired tuple to display
                if(doc.docID & (doc.docName == docno)):
                    toke.desiredTuple = tuple
                    
                toke.tupleList.append(tuple) # add to list
                
                # assign number of documents that contain term
                if(toke.frequency != 0):
                    docCount = docCount + 1
                if(wordCount != 0):
                    termFrequency = currF/wordCount
                toke.tfList.append(termFrequency)
                
            toke.docsWithTerm = docCount
    return toke

# returns document structure
def findDocument(docName):
    for x in documents:
        if(docName == x.docName):
            return x

# returns token structure
def findTerm(termName):
    blank = token()
    for y in tokens:
        if(termName == y.term):
            return y
    return blank

# handles document input
def handle_doc(doc):
    currDoc = Document()
    currDoc = findDocument(doc)
    print("\nListing for document: " + currDoc.docName)
    print("DOCID: " + str(currDoc.docID))
    print("Total terms: " + str(currDoc.totalTerms) + "\n")

# handles term input
def handle_term(word):
    emptyDoc = Document()
    currTerm = token()
    currTerm = findTerm(word)
    currTerm = getIndex(currTerm, emptyDoc)
    print("\nListing for term: " + currTerm.term)
    print("Term ID: " + str(currTerm.termID))
    print("Number of documents containing term: " + str(currTerm.docsWithTerm))
    print("Term frequency in corpus: " + str(currTerm.frequency) + "\n")

# handles doc and term input
def handle_index(term, doc):
    currDoc = Document()
    currDoc = findDocument(doc)
    currTerm = token()
    currTerm = findTerm(term)
    currTerm = getIndex(currTerm, currDoc)
    print("\nInverted list for term: " + currTerm.term)
    print("In document: " + currDoc.docName)
    print("TERMID: " + str(currTerm.termID))
    print("DOCID: " + str(currDoc.docID))
    print("Term frequency in document: " + str(currTerm.docFrequency))
    print("Positions: " + str(currTerm.desiredTuple[2]) + "\n")

# handles TF
def getTF(word):
    emptyDoc = Document()
    currTerm = token()
    currTerm = findTerm(word)
    if(len(currTerm.tfList) > 1):
        currTerm.tfList.clear()
    currTerm = getIndex(currTerm, emptyDoc)
    return currTerm.tfList

# handles DF
def getDF(word):
    emptyDoc = Document()
    currTerm = token()
    currTerm = findTerm(word)
    currTerm = getIndex(currTerm, emptyDoc)
    DF = 1 + (math.log((len(documents)/currTerm.docsWithTerm),2))
    return DF

def getDocSize():
    return len(documents)

def findDocNum(id):
    for x in documents:
        if(id == x.docID):
            return x.docName
