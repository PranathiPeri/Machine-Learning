import csv
import sys
import os
import math
import random
import re
counter=0
k=int(sys.argv[1])
input_file=sys.argv[2]
output_file=sys.argv[3]
## Function to calculate the SSE
def calSSE(means,cluster):
    sse=0
    for i in range(len(means)):
        for j in range(len(cluster[i])):
            sse=(pow(float(cluster[i][j][1])-float(means[i][0]),2)+pow(float(cluster[i][j][2])-float(means[i][1]),2))
    return sse;
## Reading from the input file
infile = open(input_file)
fh = infile.readlines()
lines = list()
for row in fh:
    x=re.split(r'[ \t \n|;"]+', row)
    lines.append(x[0:3])
flag=0
##Generating random cluster centers
means=list()
for i in range(k):
 r= random.randint(1,len(lines)-1)
 means.append(lines[r][1:3])
newL = []
for line in means:
    newL.append([float(i) for i in line])
means=newL
## Calculating the Euclidean distance and finding new cluster centers
while ((flag==0) & (counter<25)):
    count=0
    counter=counter+1
    cluster = [[] for i in range(k)]
    for i in range(1,len(lines)):
        d=list()
        for j in range(len(means)):
            x=math.sqrt(pow(float(lines[i][1])-float(means[j][0]),2)+pow(float(lines[i][2])-float(means[j][1]),2))
            d.append(x)
        cluster[d.index(min(d))].append(lines[i])

    temp_mean1=list()
    for i in range(len(cluster)):
        mean1=0
        mean2=0
        temp_mean=list()

        for j in range(len(cluster[i])):
            mean1=mean1+float(cluster[i][j][1])
            mean2=mean2+float(cluster[i][j][2])
        #print(len(cluster[i]))
        temp_mean.append(mean1/(1+len(cluster[i])))
        temp_mean.append(mean2/ (1+len(cluster[i])))
        temp_mean1.append(temp_mean)
    for z in range(len(means)):
        if((temp_mean1[z][0]==means[z][0]) & (temp_mean1[z][1]==means[z][1])):
            count=count+1
    if(count==len(means)):
        flag=1
    means=temp_mean1

#print(cluster)
#print(cluster[1][0:])
#print(calSSE(means,cluster))

file = open(output_file,"w")
for i in range(len(cluster)):
    file.write('Cluster : ')
    file.write( str(i + 1))
    file.write('\n')
    for j in range(len(cluster[i])):
        file.write(str(cluster[i][j][0]))
        file.write(',')
    file.write('\n')
file.write('\n')
file.write('\n')
file.write('The value of SSE :')
file.write(str(calSSE(means,cluster)))
file.close
#file = open("pytest.txt","w")
#file.write(cluster[])

