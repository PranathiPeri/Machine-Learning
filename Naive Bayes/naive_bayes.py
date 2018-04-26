import sys
import os
import math
import re
import collections


path =sys.argv[1]
test_path = sys.argv[2]
vocab = list()            # List  which contains the vocabulary
class_count=list()        #Count of number of files in each class  in train set
class_names=list()        #Names of each class in training set
class_list=list()         #list of Words in each class
class_word_counter=list() #List of word count in each class
test_class_count=list()   #Count of number of files in each class in test set
acc_counter=0.0           # Counter for accurarcy
for root, dirs, files in os.walk(path): #To read each file in each directory of the root
    counter=0             # To count number of files in each class
    temp_list=list()
    for file in files:
        counter+=1
        with open(os.path.join(root, file), "r") as auto:
            fh = auto.readlines()
            temp=0
            for line in fh:
                if (temp==0): # searching for Lines keyword in the file
                    if(line.startswith('Lines')):
                        temp=1
                else:    #Extracting the words from each file
                    line=re.sub('[^a-zA-Z0-9\n\']',' ',line)
                    vocab.extend(line.strip().split())
                    temp_list.extend(line.strip().split())
    class_list.append(temp_list) #Appending the words of each class
    class_count.append(counter)  # Appending the word count
    class_names.extend(dirs)     # Getting the class Names
class_count=class_count[1:]     # The no of files in each  class
class_list=class_list[1:]       #The words in each class
vocab=set(vocab)                # The unique words in the vocabulary
total_count=float(sum(class_count))  # Total number of files in the training dataset
for k in range(len(class_list)):  # To find the count of the words in class
    word_count=list()
    word_count =collections.Counter(class_list[k])
    class_word_counter.append(word_count)

for root, dirs, files in os.walk(test_path):
    counter=0.0
    temp_list=list()
    for file in files:
        counter+=1
        vocab1 = list()
        with open(os.path.join(root, file), "r") as auto:
            fh = auto.readlines()
            temp=0
            for line in fh:
                if (temp==0):
                    if(line.startswith('Lines')):
                        temp=1
                else:
                    line=re.sub('[^a-zA-Z0-9\n\']',' ',line)
                    vocab1.extend(line.strip().split())
        log_sum=list()
        for k in range(len(class_word_counter)):
            sum=0.0
            for word in vocab1:
               sum+=math.log((class_word_counter[k][word]+1.0)/(len(class_list[k])+len(vocab)))#Finding likelihood
            sum+=math.log(class_count[k]/total_count) # finding prior probability
            log_sum.append(sum)
        if((class_names[log_sum.index(max(log_sum))]) in root):
            acc_counter+=1
    test_class_count.append(counter)
test_class_sum = 0.0
# finding the no of files in the test dataset
for n in range(len(test_class_count)):
    test_class_sum+=test_class_count[n]
#Finding the Accuracy
accuracy = acc_counter/test_class_sum
print("Accuracy =",accuracy*100)
             

