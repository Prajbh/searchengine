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

dist_freq = {}
docs_freq = {}
tf = {}

gets = []
counts = []
count = 0

#get the start time of the program
prev = time.time()

#file counter
idx=0

#5 character ngram
ngram_no = 5

print("Processing part")

# iterate through all the .html files in the directory
for file in os.listdir(input_dir):
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

        # trim all whitespace
        text = re.sub(r'\s+', ' ', text)

        # file_tokens = set()
        # store all the token frequencies for each file
        dist_freq[file] = {}

        # term frequency weight of tokens for each file
        tf[file] = {}

        #length of the tokens
        length = len(text) - ngram_no
        # create hashmap with frequency and document count and iterate all tokens
        for i in range(length):
            #extract 5 token characters
            token = text[i:i+ngram_no]
            token = token.lower()

            #create frequency distribution hashmap
            if token in dist_freq[file]:
                dist_freq[file][token] += 1
            else:
                dist_freq[file][token] = 1

            # create docuemnt frequency using hashmap
            if token in docs_freq:
                if file not in docs_freq[token]:
                    docs_freq[token].append(file)
            else:
                docs_freq[token] = [file]

        for token in dist_freq[file]:
            # calculate term frequency weights, tf = f(d,w)/|D|
            wordtf = (dist_freq[file][token] * ngram_no)/length
            tf[file][token] = wordtf

        # find the elapsed time
        if idx in [10, 20, 40, 80, 100, 200, 300, 400, 500]:
            print(time.time() - prev)
            gets = time.time() - prev

        # increment file counter
        idx += 1
        counts = idx

# total number of documents
collection = idx

idx = 0

# get the programs start time
prev = time.time()

print("Calculating weights:")

# calculate and store tf-idf weights of tokens
for file in dist_freq:
    # tf-idf for each token
    tfidf = {}
    tokens = dist_freq[file]

    for i in tokens:
        # calculate idf = |c|/df(w)
        idf = math.log(collection/len(docs_freq[i]))
        # calculate tfidf = tf(d,w) * idf(w)
        tfidf[i] = tf[file][i] * idf

    if idx in [10, 20, 40, 80, 100, 200, 300, 400, 500]:
        print(time.time() - prev)
        gets = time.time() - prev
    idx += 1

    # write tfidf weights into a file
    file_write = codecs.open(os.path.join(output_dir, file) + ".ngram.wts", 'w', encoding='ascii', errors="ignore")
    # sort tokens in descending order of the tfidf weights
    sort_tokens = sorted(tfidf.items(), key=lambda kv: kv[1], reverse=True)
    for i, tfidf in sort_tokens:
        # write weights to wts file
        file_write.write(i + "\t" + str(tfidf) + "\n")
    # close file
    file_write.close()

'''
# print (gets)
# plotting

plt.plot(gets, counts)
plt.xlabel('Time Taken')
plt.ylabel('No. of files')
plt.title('Efficiency')
'''