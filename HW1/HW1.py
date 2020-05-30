#This code is written using html2text as the parser

#from __future__ import division, unicode_literals
import nltk
import os
import sys
import codecs
import html2text as htm
from collections import Counter
import re
import time
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


# check for command line arguments, must have input and output directory path
if len(sys.argv) != 3:
    print("2 arguments required: input and output directory path.")
    exit()

# get input directory
input_dir = sys.argv[1]
#input_dir = r'''/Users/prajnabhandary/Desktop/files'''
#get output directory
output_dir = sys.argv[2]
#output_dir =  r'''/Users/prajnabhandary/Desktop/output/output'''


#all possible characters we want to exclude
escape_char = ["\n","\t","\r",",",".","/","-","_","'",'"',"`","[","]","(",")","?",":","|","*",";","!","{","}",">","$","=","%","#","+","<","&","\\","0","1","2","3","4","5","6","7","8","9"]

freq_char = {}
gets = []
counts = []
count = 0

# get programs start time
prev = time.time()

for file in os.listdir(input_dir):
    if file.endswith(".html"):
        #ascii encoding
        file_asci = open(os.path.join(input_dir, file), "r", encoding="ascii", errors="ignore")
        file_read = file_asci.read()
        #use html parser to extract text from the read file
        text = htm.html2text(file_read)
        #make sure there are no unwanted characters by replacing them
        for unw in escape_char:
            text = text.replace(unw, " ")
        
        #tokenizing the strings by whitespace
        tokens = text.split(' ')
        
        file_tokens = set()
        
        #using hashmap to get the word frequency
        for i in tokens:
            if len(i) > 0:
                #convert all characters to lower case
                i = i.lower()
                file_tokens.add(i)
                
                if i in freq_char:
                    freq_char[i] = freq_char[i] + 1
                else:
                    freq_char[i] = 1
         
        #write the tokens into a file
        file_write = codecs.open(os.path.join(output_dir, file) +".txt", 'w', encoding='ascii',errors="ignore")
        for i in file_tokens:
            file_write.write(i+"\n")
            
        # close the file
        file_write.close()
        
    # find elapsed CPU time at every 50th file to plot in graph.
    if count % 50 == 0:
        #print(time.time() - prev)
        get = time.time() - prev
        gets.append(get)
        counts.append(count)
    # increment file counter
    count+=1  
    
# sort tokens in an alphabettical order  
sort_tokens = sorted(freq_char.items(), key=lambda kv: kv[0])

# save to file dist_tokens.txt
fw = codecs.open("dist_tokens.txt", 'w', encoding='ascii',errors="ignore")
for i in sort_tokens:
    fw.write(i[0] + " " + str(i[1]) +"\n")
fw.close()

# sort tokens according to highest frequency
sort_vals = sorted(freq_char.items(), key=lambda kv: kv[1], reverse=True)

# save to file dist_freq.txt
fw = codecs.open("dist_freq.txt", 'w', encoding='ascii',errors="ignore")
for i in sort_vals:
    fw.write(i[0] + " " + str(i[1]) + "\n")
fw.close()

#print (gets)
# plotting

plt.plot(gets, counts)
plt.xlabel('Time Taken')
plt.ylabel('No. of files')
plt.title('Efficiency')
