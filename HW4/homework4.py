# This code is written using html2text as the parser

# from __future__ import division, unicode_literals
import nltk
import os
import sys
import codecs
import html2text as htm
from collections import Counter
import re
import time
import math

# check for command line arguments, must have input and output directory path
if len(sys.argv) < 2:
    print("pass at least one query as argument")
    exit()

#the postings.txt and input.txt files are considered from homework 3 to keep track of the inverted index

#choose to add term weights
score = False
if sys.argv[1] == "Wt":
    score = True
    if len(sys.argv) < 4: #at least two query with their term weights
        print("Need the term weights for weight query")

# all possible characters we want to exclude
escape_char = ["\n", "\t", "\r", ",", ".", "/", "-", "_", "'", '"', "`", "[", "]", "(", ")", "?", ":", "|", "*", ";",
               "!", "{", "}", ">", "$", "=", "%", "#", "+", "<", "&", "\\", "0", "1", "2", "3", "4", "5", "6", "7", "8",
               "9"]


# read the stopwords from the file
stopwordfile = open("stopwords.txt", "r")
stopwordlist = stopwordfile.read()
stopwordlist = stopwordlist.replace("'", "")
stopwordlist = stopwordlist.split("\n")

query = {}

#remove the stopwords
def removestop(text):

     # make sure there are no unwanted characters by replacing them
    for unw in escape_char:
        text = text.replace(unw, " ")

    text = text.strip().lower()
    if len(text) and text not in escape_char:
        return text


if score:
    for i in range(3,len(sys.argv),2):
        text = removestop(sys.argv[i])
        if text:
            query[text] = float(sys.argv[i-1])
else:
    for i in range(1,len(sys.argv)):
        text = removestop(sys.argv[i])
        if text:
            query[text] = 1

#open the postings.txt file from homework 3
post_file = open(os.path.join("output", "postings.txt"), "r", encoding="ascii", errors="ignore")
postings = post_file.read()
post_file.close()
postings = postings.split("\n")

#open the index.txt file
index_file = open(os.path.join("output", "index.txt"), "r", encoding="ascii", errors="ignore")
index = index_file.read()
index_file.close()
index = index.split("\n")

result = {}

#consider every query word
for token, weight in query.items():
    if token in index:
        #if the word was found in the index file consider the frequency and teh position of the file
        id = index.index(token)
        freq = int(index[id + 1])
        pos = int(index[id + 2])
        #use hash table for document-query similarity scores
        doclist = postings[pos:pos + freq]
        for a in doclist:
            [doc, idf] = a.split("\t")
            if doc not in result:
                result[doc] = 0
            result[doc] += float(idf) * weight

#sort the document results
result_sorted = sorted(result.items(), key=lambda kv: kv[1], reverse=True)
#filter the documents that have the queried words
filter_res = list(filter(lambda kv: kv[1] > 0, result_sorted))
#only print the top 10 documents else print the query is not found
if len(filter_res):
    count = min(10, len(filter_res))
    for i in range(count):
        print(filter_res[i][0], filter_res[i][1])
else:
    print("No results")

'''
# print (gets)
# plotting

plt.plot(gets, counts)
plt.xlabel('Time Taken')
plt.ylabel('No. of files')
plt.title('Efficiency')
'''