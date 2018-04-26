import csv
import sys
import os
import math
import random
import re
import numpy as np


# Reading Input File and different parameters
neurons=list()
input_file=sys.argv[1]
error_tol = float(sys.argv[3])
train_per = float(sys.argv[2])
no_of_layers = int(sys.argv[4])
for k in range(no_of_layers):
    neurons = neurons + [int(sys.argv[5+k])]

infile = input_file
fh = csv.reader(open(infile))
data = list()
train_data = list()
test_data = list()
eta=0.1
error=1.0
counter=0

#Sigmoid Function
def sigmoid(x):
    try:    
        sig = 1.0/(1+math.exp(-x))
        return sig
    except OverflowError:
        if(x>0):
            return 1
        else:
            return 0

for row in fh:
    if("\n" not in row):
        data.append(row)
#selecting training_set and test set
train_per = train_per/100.0
train = int(train_per*len(data)+0.5)
random.shuffle(data)
train_data = data[:train]
test_data = data[train:]

input_train=list()
target_train=list()

input_test=list()
target_test=list()

for row in train_data:
    input_train.append(row[:-1])
    target_train.append(row[len(data[0])-1])

for row in test_data:
    input_test.append(row[:-1])
    target_test.append(row[len(data[0])-1])


weights=list()
input=len(input_train[0])+1


#generating random weights for hidden layer
for i in range(no_of_layers):
    output=neurons[i];
    temp=list()
    for j in range(input*output):
        temp.append(random.uniform(0,1))
    weights.append(temp)
    input=output+1
temp=list()
output=1
#generating random weights for output layer
for j in range(input*output):
    temp.append(random.uniform(0,1))
weights.append(temp)

#Back propagation Algorithm for training_set
while((error>error_tol)&(counter<2000)):
    
    counter+=1
    error=0.0
    #Forward propagation
    for z in range(len(input_train)):
        temp_weights=list()
        temp_train = list()
        output_result=list()
        delta = list()
        a=1
        temp_train.append([a]+input_train[z])
        output_result.append(temp_train)
        temp_train=np.array(temp_train)
        for k in range(no_of_layers):        
            for i in range(neurons[k]):
                temp_weights.append(weights[k][(i*(len(weights[k])/neurons[k])):(i+1)*(len(weights[k])/neurons[k])])
            temp_weights=np.array(temp_weights)
            temp_train=temp_train.astype(np.float)
            temp_train=np.transpose(temp_train)
            temp_result=np.matmul(temp_weights,temp_train)
            temp_result=np.transpose(temp_result)
            temp_result=temp_result.tolist()
            temp_result=temp_result[0]
            net_result=list()
            for i in range(len(temp_result)):
                b=(sigmoid(temp_result[i]))
                net_result=net_result+[b]
            temp_weights=list()
            temp_train = list()
            temp_train.append([a]+net_result)
            output_result.append(temp_train)
            temp_train=np.array(temp_train)
        temp_weights.append(weights[k+1])    
        temp_weights=np.array(temp_weights)
        temp_train=temp_train.astype(np.float)
        temp_train=np.transpose(temp_train)
        temp_result=np.matmul(temp_weights,temp_train)
        temp_result=np.transpose(temp_result)
        temp_result=temp_result.tolist()
        temp_result=temp_result[0]
        net_result=list()
        for i in range(len(temp_result)):
           b=(sigmoid(temp_result[i]))
           net_result=net_result+[b]
        temp_delta=(net_result[0])*(1-net_result[0])*(float(target_train[z])-net_result[0])
        #training set error calculation
        error+=((float(target_train[z])-net_result[0])*(float(target_train[z])-net_result[0])*0.5/len(input_train))
        delta.append(temp_delta)
        #backward propagation
        for j in range(no_of_layers):
            temp1_delta=list()
            new_weights=list()
            for d in range(neurons[len(neurons)-j-1]+1):
                h=weights[len(weights)-j-1]
                temp_h = list()
                temp_delta=list()
                
                for i in range(len(h)/len(delta)):
                    temp_h.append(h[(i*(len(delta))):(i+1)*(len(delta))])
                temp_h=np.array(temp_h)
                temp_h=np.transpose(temp_h)
                temp_delta.append(delta)
                temp_delta=np.array(temp_delta) 
                h1=np.matmul(temp_delta,temp_h)
                h1=h1.tolist()
                h1=h1[0][d]
                temp_delta1=(output_result[len(output_result)-j-1][0][d])*(1-(output_result[len(output_result)-j-1][0][d]))*(float(h1))
                temp1_delta.append(temp_delta1)
            for d2 in range(len(delta)):
                for d1 in range(neurons[len(neurons)-j-1]+1):
                    temp_new_weight=eta*delta[d2]*(output_result[len(output_result)-j-1][0][d1])
                    new_weights.append(temp_new_weight)
            for i in range(len(weights[len(weights)-j-1])):
                weights[len(weights)-j-1][i]=weights[len(weights)-j-1][i]+new_weights[i]
            delta=temp1_delta[1:]
        for d2 in range(len(delta)):
            for d1 in range(len(input_train[0])):
                temp_new_weight=eta*delta[d2]*(float(input_train[z][d1]))
                new_weights.append(temp_new_weight)
        for i in range(len(weights[0])):
                weights[0][i]=weights[0][i]+new_weights[i]
        
error_test=0.0 
#back propagation algorithm for test_set   
for z in range(len(input_test)):
    temp_weights=list()
    temp_train = list()
    output_result=list()
    delta = list()
    a=1
    temp_train.append([a]+input_test[z])
    output_result.append(temp_train)
    temp_train=np.array(temp_train)
    for k in range(no_of_layers):        
        for i in range(neurons[k]):
            temp_weights.append(weights[k][(i*(len(weights[k])/neurons[k])):(i+1)*(len(weights[k])/neurons[k])])
        temp_weights=np.array(temp_weights)
        temp_train=temp_train.astype(np.float)
        temp_train=np.transpose(temp_train)
        temp_result=np.matmul(temp_weights,temp_train)
        temp_result=np.transpose(temp_result)
        temp_result=temp_result.tolist()
        temp_result=temp_result[0]
        net_result=list()
        for i in range(len(temp_result)):
            b=(sigmoid(temp_result[i]))
            net_result=net_result+[b]
        temp_weights=list()
        temp_train = list()
        temp_train.append([a]+net_result)
        output_result.append(temp_train)
        temp_train=np.array(temp_train)
    temp_weights.append(weights[k+1])    
    temp_weights=np.array(temp_weights)
    temp_train=temp_train.astype(np.float)
    temp_train=np.transpose(temp_train)
    temp_result=np.matmul(temp_weights,temp_train)
    temp_result=np.transpose(temp_result)
    temp_result=temp_result.tolist()
    temp_result=temp_result[0]
    net_result=list()
    for i in range(len(temp_result)):
        b=(sigmoid(temp_result[i]))
        net_result=net_result+[b]
    temp_delta=(net_result[0])*(1-net_result[0])*(float(target_train[z])-net_result[0])
    #test set error calculation
    error_test+=((float(target_test[z])-net_result[0])*(float(target_test[z])-net_result[0])*0.5/len(input_test))
    delta.append(temp_delta)

for i in range(no_of_layers):
    print("")
    print("Hidden Layer"+str(i+1)+":")
    print('\t'),
    for j in range(neurons[i]):
        print ("Neuron"+str(j+1) + ":"),
        print weights[i][j*len(weights[i])/neurons[i]:(j+1)*len(weights[i])/neurons[i]]
        print("\t"),
i+=1
print("")
print("Output Layer"+":")
print('\t'),

print ("Neuron1"+ ":"),
print weights[i]


print ("train error:"),
print (error)

print ("test error:"),
print (error_test)
