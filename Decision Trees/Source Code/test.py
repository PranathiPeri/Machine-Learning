import csv
import sys
import os
import math
import random

train_s = sys.argv[1]
valid_s = sys.argv[2]
test_s = sys.argv[3]
pru_fac = float(sys.argv[4])
data = csv.reader(open(train_s ))
test_data = csv.reader(open(test_s))
valid_set = csv.reader(open(valid_s))
lines = list()
test_lines = list()
valid_lines = list()
counter=0.0
node_count1=0
node_count=0
leaf_count=0
space_count=0
for r in data:
    lines.append(r)
for r in valid_set:
    valid_lines.append(r)
for r in test_data:
    test_lines.append(r)
def info_gain_cal(lines):                           # Method to calculate Information Gain
    class_entropy=0.0
    siz_row = len(lines[0])
    cla = list()
    for j in range(1,  (len(lines))):
        cla.append(lines[j][siz_row-1])
    count1 = 0
    for k in range(len(cla)):
        if (cla[k]=='1'): 
            count1+=1
    count0 = (len(cla)-count1)
    a = float(count0)/len(cla)
    b = float(count1)/len(cla)
    if(a==0):
        a=1
    if(b==0):
        b=1
    class_entropy = (-a)*(math.log(a, 2)) + (-b)*(math.log(b, 2))
    info_gain = list()
    for j in range(siz_row-1): 
        count_col0 = 0.0
        count_col00 = 0.0
        count_col01 = 0.0
        count_col1 = 0.0
        count_col10 = 0.0
        count_col11 = 0.0
        gain = 0.0
        for k in range(1, len(lines)):
            if (lines[k][j]=='1'):   
                count_col1+=1
                if (lines[k][siz_row-1]=='1'):    
                    count_col11+=1
                else:
                    count_col10+=1
            else:
                count_col0+=1
                if (lines[k][siz_row-1]=='1'):    
                    count_col01+=1
                else:
                    count_col00+=1
        if((count_col01==0)|(count_col00==0)):
            if((count_col10==0)|(count_col11==0)):
                gain=class_entropy
            else:
                gain = class_entropy + (count_col1/len(cla))*((count_col10/count_col1*math.log(count_col10/count_col1, 2))  +(count_col11/count_col1*math.log(count_col11/count_col1, 2)))
        elif((count_col10==0)|(count_col11==0)):
            gain = class_entropy + (count_col0/len(cla))*((count_col00/count_col0*math.log(count_col00/count_col0, 2))+(count_col01/count_col0*math.log(count_col01/count_col0, 2))) 
        else:
            gain = class_entropy + (count_col1/len(cla))*((count_col10/count_col1*math.log(count_col10/count_col1, 2))  +(count_col11/count_col1*math.log(count_col11/count_col1, 2))) + (count_col0/len(cla))*((count_col00/count_col0*math.log(count_col00/count_col0, 2))+(count_col01/count_col0*math.log(count_col01/count_col0, 2))) 
        info_gain.append(gain)
    return lines[0][info_gain.index(max(info_gain))]
    
test=info_gain_cal(lines)

# Defining a Class for Tree
class Tree:
    def __init__ (self):                                        # Constructor of class
        self.root=None
    def insert (self, attr):                                  # Method to insert a node in the Tree
        if (self.root):
            return self.root.insert(attr)
        else:
            self.root = Node(attr)
            return self.root.insert(lines)
    def find (self, attr1):                                   # Method to find a node in the Tree
        if (self.root):
            return self.root.find(attr1)
        else:
            return 0
    def prin (self):                                            # Method to print a  Tree
        if(self.root):
            return self.root.prin()
        else:
            return 0
    def delete (self, n_num):                           # Method to delete a node in the Tree
        if(self.root):
            return self.root.delete(n_num)
        else:
            return 0
#Defining a class for Node
class Node:
    def __init__ (self, val):                                # Constructor of a node
        self.value=val
        global node_count
        self.split1=list()
        self.split0=list()
        node_count+=1
        self.number=node_count
        self.leftnode=None
        self.rightnode=None
    def insert(self, data):                                # Method to insert a node
        value1=data[0].index(self.value)
        self.split1.append(data[0][:value1]+data[0][(value1+1):])
        for row in data:
            if(row[value1]=='1'):
                self.split1.append(row[:value1]+row[(value1+1):])
            else:
                self.split0.append(row[:value1]+row[(value1+1):])
        
        if((len(self.split0)>1)&(len(self.split0[0])>1)):
            flag=0
            for z in range(1, len(self.split0)):
                if((self.split0[z][len(self.split0[0])-1])==(self.split0[1][len(self.split0[0])-1])):
                    flag+=1
                else:
                    flag+=0
            if(flag!=(len(self.split0)-1)):
                
                self.leftnode = Node(info_gain_cal(self.split0))
                self.leftnode.insert(self.split0)
            else:
                
                self.leftnode = Node(self.split0[1][len(self.split0[0])-1])
                
        else:
            
            if(len(self.split0)==1):
                self.leftnode=Node('1')
            else:
                
                self.leftnode = Node(self.split0[1][len(self.split0[0])-1])
            
        if((len(self.split1)>1)&(len(self.split1[0])>1)):
            flag=0
            for z in range(1, len(self.split1)):
                if((self.split1[z][len(self.split1[0])-1])==(self.split1[1][len(self.split1[0])-1])):
                    flag+=1
                else:
                    flag+=0
            if(flag!=(len(self.split1)-1)):
                
                self.rightnode = Node(info_gain_cal(self.split1))
                self.rightnode.insert(self.split1)
            else:
                
                self.rightnode = Node(self.split1[1][len(self.split1[0])-1])
                
        else:
            
            if(len(self.split1)==1):
                self.rightnode=Node('0')
            else:
                
                self.rightnode = Node(self.split1[1][len(self.split1[0])-1])
            
        return 1
    def find(self, test_row):                           # Method to find a node in the Tree
        row=list()
        row.append(test_lines[0])
        row.append(test_row)
        global counter
        if((self.value=='1')|(self.value=='0')):
            if(self.value==test_row[len(test_row)-1]):
                counter+=1
        else:    
            for z in range(len(row[0])):
                if((self.value==row[0][z])):
                    if(test_row[z] == '1'):
                        if((self.value!='1')|(self.value!='0')):
                            self.rightnode.find(test_row)
                    elif(test_row[z]=='0'):
                        if((self.value!='0')|(self.value!='1')):
                            self.leftnode.find(test_row)
        return 1   
    def prin (self):                                    # Method to print a node in the Tree
        global space_count
        global leaf_count
        global node_count1
        node_count1+=1
        for k in range(space_count):
                print("|"),
        print(self.value + " = 0 :"), 
        if((self.leftnode.value!='0')&(self.leftnode.value!='1')):
            print('')
            space_count+=1
            self.leftnode.prin()
            space_count-=1
        else:
            node_count1+=1
            print(self.leftnode.value)
            leaf_count+=1
        for k in range(space_count):
                print("|"),
        print(self.value + " = 1 :"), 
        if((self.rightnode.value!='0')&(self.rightnode.value!='1')):
            print('')
            space_count+=1
            self.rightnode.prin()
            space_count-=1
        else:
            node_count1+=1
            print(self.rightnode.value)
            leaf_count+=1
    def delete(self, n_num):                                #deleting a nodes according to given pruning factor
        temp_split=list()
        count0=0
        count1=0
        if(self.number==n_num):
            self.leftnode=None
            self.rightnode=None
            temp_split.append(self.split0)
            temp_split.append(self.split1)
            for k in range(1, len(temp_split)-1):
                if(temp_split[k][len(temp_split[0])-1]=='1'):
                    count1+=1
                else:
                    count0+=1
            if(count1>count0):
                self.value='1'
            else:
                self.value='0'
        if((self.value!='0')&(self.value!='1')):
            self.leftnode.delete(n_num)
            self.rightnode.delete(n_num)
        return 1
                    
tree = Tree()                                               # Creating a Tree
tree1=tree.insert(test)
tree.prin()
print('\n')
test_count=0.0
for row in range(1, len(lines)):
    tree.find(lines[row])
accuracy=counter/(len(lines)-1)
print("_________________________________________________________________")
print("Before pruning")
print("_________________________________________________________________")
print("Number of Training Instances :"+`len(lines)-1`)
print("Number of Training Attributes:"+`len(lines[0])-1`)
print("Total Number of nodes in the tree:"+`node_count1`)
print("Number of leaf nodes in the tree:"+`leaf_count`)
print("Accuracy of the model on the training set:"+`accuracy*100`)
print('\n')
counter=0.0
accuracy_valid=0.0
for row in range(1, len(valid_lines)):
    tree.find(valid_lines[row])
accuracy_valid=counter/(len(valid_lines)-1)
print("Number of validation instances:"+`len(test_lines)-1`)
print("Number of validation attributes:"+`len(test_lines[0])-1`)
print("Accuracy of the model on the validation data set before pruning:"+`accuracy_valid*100`)
print('\n')
counter=0.0
for row in range(1, len(test_lines)):
    tree.find(test_lines[row])
accuracy=counter/(len(test_lines)-1)
print("Number of testing instances:"+`len(test_lines)-1`)
print("Number of testing attributes:"+`len(test_lines[0])-1`)
print("Accuracy of the model on the testing data set:"+`accuracy*100`)
print('\n\n')
leaf_count = 0
node_count1=0
ran_flag=0
check=0
accuracy1=0.0
accuracy2=0.0
accuracy3=0.0
check_count=0
while((check==0)&(check_count<200)):
    check_count+=1
    ran=random.sample(range(1, node_count+1), (int)((node_count*pru_fac)+0.5))
    while (ran_flag==0):
        for k in ran:
            if(k==1):
                ran_flag=1
        if(ran_flag==1):
            ran=random.sample(range(1, node_count+1), (int)((node_count*pru_fac)+0.5))
            ran_flag=0
        else:
            ran_flag=1
    
    for k in ran:
        tree.delete(k)
    counter=0.0
    for row in range(1, len(lines)):
        tree.find(lines[row])
    accuracy1=counter/(len(lines)-1)
    
    counter=0.0
    for row in range(1, len(valid_lines)):
        tree.find(valid_lines[row])
    accuracy2=counter/(len(valid_lines)-1)
    if(accuracy2>accuracy_valid):
        check=1
    else:
        check=0
        tree=Tree()
        tree.insert(test)
    
    counter=0.0
    for row in range(1, len(test_lines)):
        tree.find(test_lines[row])
    accuracy3=counter/(len(test_lines)-1)
    
tree.prin()
if(check_count==200):
    print("tested with 200 random samples to produce more accuracy after pruning than before, given pruning factor is not effective")
print('\n')
print("_________________________________________________________________")
print("After pruning")
print("_________________________________________________________________")
print("Number of Training Instances :"+`len(lines)-1`)
print("Number of Training Attributes:"+`len(lines[0])-1`)
print("Total Number of nodes in the tree:"+`node_count1`)
print("Number of leaf nodes in the tree:"+`leaf_count`)
print("Accuracy of the model on the training set:"+`accuracy1*100`)
print('\n')

print("Number of validation instances:"+`len(test_lines)-1`)
print("Number of validation attributes:"+`len(test_lines[0])-1`)
print("Accuracy of the model on the validation data set after pruning:"+`accuracy2*100`)
print('\n')

print("Number of testing instances:"+`len(test_lines)-1`)
print("Number of testing attributes:"+`len(test_lines[0])-1`)
print("Accuracy of the model on the testing data set:"+`accuracy3*100`)
