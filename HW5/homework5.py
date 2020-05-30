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
import re
import time
import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
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

docs_freq = {}
dist_freq = {}
tf = {}
id = 0
files = {}

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

        for word in stopwordlist:
            text = text.replace(" " + word + " ", " ")

        files[file] = text

#print(files.keys())

# for file in freq_dist:
#     # conatins tf-idf for each token
#     tfidf = {}
#     tokens = freq_dist[file]
#     for tok in tokens:
#         # calculate idf = |c|/df(w)
#         idf = math.log(collection/len(doc_freq[tok]))
#         # calculate tfidf = tf(d,w) * idf(w)
#         tfidf[tok] = tf[file][tok] * idf

tfidf_vectorizer = TfidfVectorizer()

#find the cosinesimilarities of the file
def cosinesimilarity(a1,a2):
    if not len(a1.strip()) and not len(a2.strip()):
        return 0
    tfidf_matrix = tfidf_vectorizer.fit_transform([a1, a2])
    return ((tfidf_matrix * tfidf_matrix.T).A)[0, 1]

cosinesimilarity(files["001.html"], files["002.html"])

cos_sim_matrix = {}
for file1 in files:
    #print(file1)
    cos_sim_matrix[file1] = {}
    for file2 in files:
        if file1 == file2: #if same files then break
            break
        cos_sim_matrix[file1][file2] = cosinesimilarity(files[file1], files[file2])

#consider the initial centroids as the files themselves
def initial_centroids(files):
    centroids = {}
    for i in files:
        centroids[i] = [i]
    return centroids

#find the files that are most similer
def near_cluster(centroid, doc_vec):
    maxi = -1
    max_n = (maxi, 0, 0)
    for k1 in centroid.keys():
        for k2 in centroid[k1].keys():
            #check if already exists in the queue
            if k1 != k2 and k1 not in doc_vec and k2 not in doc_vec:
                score = centroid[k1][k2]
                if score > maxi:
                    maxi = score
                    max_n = (maxi, k1, k2)
    return max_n

#find the files that are most dissimilar
def far_cluster(centroid, doc_vec):
    mini = 6000
    minn = (mini, 0, 0)
    for d1 in centroid.keys():
        for d2 in centroid[d1].keys():
            #check if already exists in queue
            if d1 != d2 and d1 not in doc_vec and d2 not in doc_vec:
                score = centroid[d1][d2]
                if score < mini:
                    mini = score
                    minn = (mini, d1, d2)
    return minn

#print the most similar and dissimilar files
print(near_cluster(cos_sim_matrix, set()))
print(far_cluster(cos_sim_matrix, set()))

#clusing algorithm to merge the similar files

def hierarchial(clusters, centroid):
    doc_vec = set()
    leng_clusters = len(clusters.keys())

    while leng_clusters - len(doc_vec) - 1:
        cname = str(leng_clusters)
        cosine_score, c1, c2 = near_cluster(centroid, doc_vec)
        if cosine_score != -1:
            new_cluster = [c1, c2]
            doc_vec.update(new_cluster)
            clusters[cname] = new_cluster
            centroid[cname] = {}

            for cluster in clusters:
                if cluster not in doc_vec:
                    update_scores(centroid, clusters, cname, cluster)

            leng_clusters += 1
        print(c1 + "+" + c2 + "--->" + cname + "::" + str(cosine_score))

#update the scores of the merge
def update_scores(data, clusters, cname, other):
    cluster1 = clusters[cname]
    cluster2 = clusters[other]
    documents = len(cluster1) + len(cluster2)
    score = 0
    for doc1 in cluster1:
        for doc2 in cluster2:
            if doc1 in data and doc2 in data[doc1]:
                score += data[doc1][doc2]
            if doc2 in data and doc1 in data[doc2]:
                score += data[doc2][doc1]

        data[cname][other] = score / documents

#set the initial centroids
centroids = initial_centroids(files)
hierarchial(centroids, cos_sim_matrix)
# file_tokens = set()
# store all the token frequencies for each file
output = open(os.path.join(output_dir, "cluster.json"),"w")
output.write(str(centroids).replace("'", '"'))
output.close()

'''
# print (gets)
# plotting

plt.plot(gets, counts)
plt.xlabel('Time Taken')
plt.ylabel('No. of files')
plt.title('Efficiency')
'''