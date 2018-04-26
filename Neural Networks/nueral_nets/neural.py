import csv
import sys
import os
import math
import random
import re
import numpy as np


# Reading Input File and finding the delimiter
input_file=sys.argv[1]
output_file=sys.argv[2]
infile = open(input_file)
fh = infile.readlines()
lines = list()
lines1 = list()
for row in fh:
    x=re.split(r'[ ,|;"]+', row)
    if(x[0]==''):
        lines.append(x[1:])
    else:
        lines.append(x)
#Removing Missing Values
for row in lines:
    count =0
    for r in row:
        if ((not r)or(r=='?')):
            count+=1
        else:
            count+=0
    if (count==0):
        lines1.append(row)
#Standarization  and categorical values
for r in range(len(lines1[0])):
    count=0
    sum=0.0
    temp = list()
    for row in range(len(lines1)):
        try:
            num_lines1 = float(lines1[row][r])
            count += 1
            sum += num_lines1
            temp.append(num_lines1)
        except ValueError:
            count += 0
            pass
    if(count==(len(lines1))):
        temp = np.array(temp)
        mean=np.mean(temp)
        st = np.std(temp)
        for row in range(len(lines1)):
            lines1[row][r]=(float(lines1[row][r])-mean)/st
    else:
        for row in range(len(lines1)):
            temp.append(lines1[row][r])
        temp = np.array(temp)
        uni = np.unique(temp)
        uni=uni.tolist()
        for row in range(len(lines1)):
            lines1[row][r] = uni.index(lines1[row][r])
lines2=list()
for i in range(len(lines1)):
    lines2.append(lines1[i][len(lines1[0])-1])
lines2 = np.array(lines2)
max = np.amax(lines2)
min = np.amin(lines2)
lines2 = lines2.tolist()
for i in range(len(lines1)):
    lines1[i][len(lines1[0])-1] = (float(lines1[i][len(lines1[0])-1]-min)/(max-min))
#writing the processed set to file
with open(output_file, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(lines1)




