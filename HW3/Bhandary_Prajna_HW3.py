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
#import numpy as np
#import pandas as pd
#from matplotlib import pyplot as plt

# check for command line arguments, must have input and output directory path
if len(sys.argv) != 3:
    print("2 arguments required: input and output directory path.")
    exit()

# get input directory
input_dir = sys.argv[1]
#input_dir = r'''/Users/prajnabhandary/Desktop/files'''
# get output directory
output_dir = sys.argv[2]
#output_dir = r'''/Users/prajnabhandary/Desktop/output/output'''

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# all possible characters we want to exclude
escape_char = ["\n", "\t", "\r", ",", ".", "/", "-", "_", "'", '"', "`", "[", "]", "(", ")", "?", ":", "|", "*", ";",
               "!", "{", "}", ">", "$", "=", "%", "#", "+", "<", "&", "\\", "0", "1", "2", "3", "4", "5", "6", "7", "8",
               "9"]


# read the stopwords from the file
stopwordfile = open("stopwords.txt", "r")
stopwordlist = stopwordfile.read()
stopwordlist = stopwordlist.replace("'", "")
stopwordlist = stopwordlist.split("\n")


# Storing the entry which is fixed length in an index file
class Record:
    def __init__(self, word, postings, offset):
        self.word = word
        self.postings = postings
        self.offset = offset

#select a set number of files

for check in [10, 20, 40, 80, 100, 200, 300, 400, 500]:
    docs_freq = {}
    dist_freq = {}
    tf = {}

    # file counter
    id=0

    print("Processing part")
    prev = time.time()
    # iterate through all the .html files in the directory
    for file in os.listdir(input_dir):
        #check if the number of files processed is in set
        if id == check:
            break
        #remaining files that end with .html
        if file.endswith(".html"):
            # ascii encoding
            file_asci = open(os.path.join(input_dir, file), "r", encoding="ascii", errors="ignore")
            # read the contents of the file
            file_read = file_asci.read()
            # use html parser to extract text from the read file
            text_maker = htm.HTML2Text()
            text_maker.ignore_links = True
            text_maker.ignore_images = True
            text_maker.images_to_alt = True
            text_maker.protect_links = True
            text_maker.ignore_anchors = True
            text_maker.inline_links = False
            text = text_maker.handle(file_read)

            # make sure there are no unwanted characters by replacing them
            for unw in escape_char:
                text = text.replace(unw, " ")

            # tokenizing the strings by whitespace
            tokens = text.split(' ')

            # file_tokens = set()
            # store all the token frequencies for each file
            dist_freq[file] = {}

            # term frequency weight of tokens for each file
            tf[file] = {}

            # create hashmap with frequency and document count and iterate all tokens
            for i in tokens:
                i = i.lower()
                # ignore empty tokens and stopwords
                if len(i) > 1 and i not in stopwordlist:
                    # create frequency distribution hashmap
                    if i in dist_freq[file]:
                        dist_freq[file][i] += 1
                    else:
                        dist_freq[file][i] = 1

                    # create docuemnt frequency using hashmap
                    if i not in docs_freq:
                        docs_freq[i] = set()
                    docs_freq[i].add(file)

            for i in dist_freq[file]:
                # calculate term frequency weights, tf = f(d,w)/|D|
                wordtf = dist_freq[file][i]/len(tokens)
                tf[file][i] = wordtf

            # increment file counter
            id += 1

     # find elapsed CPU time of files proccessed
    print(time.time() - prev)

    # total number of documents
    collection = id

    # get programs start time
    prev = time.time()

    print("Calculating weights:")

    # calculate and store tf-idf weights of tokens
    tfidf = {}
    for file in dist_freq:
        # tf-idf for each token
        tokens = dist_freq[file]
        tfidf[file] = {}

        for tok in tokens:
            # calculate idf = |c|/df(w)
            idf = math.log(collection/len(docs_freq[tok]))
            # calculate tfidf = tf(d,w) * idf(w)
            tfidf[file][tok] = tf[file][tok] * idf

    # find elapsed CPU time of tfidf calculation
    print(time.time() - prev)

    index = []
    postings = []

    # get programs start time
    prev = time.time()

    print("Indexing:")
    for tok in docs_freq:
        docs = docs_freq[tok]
        record = Record(tok, len(docs), len(postings) + 1)
        index.append(record)
        for doc in docs:
            weight = tfidf[doc][tok]
            postings.append((doc, weight))

    #create postings.txt file
    post_file = os.path.join(output_dir,"postings") +".txt"
    file_write = codecs.open(post_file, 'w', encoding= 'ascii', errors="ignore")
    for doc, tfidf in postings:
        #store the pairs
        file_write.write(doc + "\t" + str(tfidf) + "\n")
    # close file
    file_write.close()

    # write index.txt into a file
    index_file = os.path.join(output_dir,"index") +".txt"
    file_write = codecs.open(index_file, 'w', encoding='ascii', errors="ignore")
    for record in index:
        # store the number of documents
        file_write.write(record.word + "\n" + str(record.postings) + "\n" + str(record.offset) + "\n")
    # close file
    file_write.close()

    #elapsed time
    print("elapsed CPU time and file sizes of index and postings")
    print(time.time() - prev, os.path.getsize(index_file)/1024, os.path.getsize(post_file)/1024)

'''
# print (gets)
# plotting

plt.plot(gets, counts)
plt.xlabel('Time Taken')
plt.ylabel('No. of files')
plt.title('Efficiency')
'''