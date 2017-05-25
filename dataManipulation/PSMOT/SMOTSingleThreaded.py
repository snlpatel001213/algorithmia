# coding: utf-8

import csv
import random
from random import randint
import math
import operator
# read https://www.jair.org/media/953/live-953-2037-jair.pdf
global dataSet
# witting synthetic samples out
syntheticData = open("Synthetic.txt", "w") # to write synthetic samples
def loadDataset(filename, numattrs):
    """
    loads data from file
    :param filename:
    :param numattrs: number of column in file, Excluding  class column
    :return:
    """
    csvfile = open(filename, 'r')
    lines = csv.reader(csvfile)
    dataset = list(lines)
    for x in range(len(dataset)):
        for y in range(numattrs):
            dataset[x][y] = float(dataset[x][y])
    return dataset

def euclideanDistance(instance1, instance2, length):
    """
    calculate euclidean distance between two
    :param instance1:[6.5, 3.0, 5.8, 2.2]
    :param instance2:[6.3, 2.9, 5.6, 1.8]
    :param length: 4 length of array
    :return:
    """
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)
print euclideanDistance([6.5, 3.0, 5.8, 2.2],[6.3, 2.9, 5.6, 1.8],4)

def getNeighbors(trainingSet, eachMinorsample, k):
    """
    will give top k neighbors for given minor sample (eachMinorsample) in dataset (trainingSet)
    :param trainingSet:  here entire data-set is a training set
    :param eachMinorsample:
    :param k: number of nearest neighbors to search for each minor sample value, using Euclidean distance
    :return: top k neighbors
    
    output: # Minor Sample:  [6.3, 3.3, 6.0, 2.5, 'Iris-virginica'] | neighbors:  [[6.5, 3.0, 5.8, 2.2, 'Iris-virginica'],
        #                                                                 [6.3, 2.9, 5.6, 1.8, 'Iris-virginica'],
    """
    distances = []
    length = len(eachMinorsample) - 1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(eachMinorsample, trainingSet[x], length)  # get euclidean distance for all matches
        distances.append((trainingSet[x], dist))
        distances.sort(key=operator.itemgetter(1))  # sort as per distance and get top 3 excluding first one
        neighbors = []
    for x in range(k):
        neighbors.append(distances[x + 1][0])  # X+1 in the sorted list ensure that the minor sample itself is not selected as neighbors
    return neighbors



def seperateMinority(dataSet, MinorClassName, classColumnNumber):
    """
    will separate given minor class from the entire dataset
    :param dataSet: Entire dataset
    :param MinorClassName:  name of minor class, e.g. MinorClassName = "Iris-virginica"
    :param classColumnNumber: column number where class is present [zero indexed]
    :return:
    """
    minorSamples = []
    for eachSample in dataSet:
        if (eachSample[classColumnNumber] == MinorClassName):
            minorSamples.append(eachSample)
    return minorSamples




def SMOTE(T, N, minorSamples, numattrs, dataSet, k):
    """
    :param T = Number of minority class Samples # here we have 5
    :param k = k mean (clustering value)
    :param minorSample: all minor samples
    :param N = "Number of sample to be generated should be more than 100%"
        Amount of smoted sample required  N%
    """
    if (N <= 100):
        print "Number of sample to be generated should be more than 100%"
        raise ValueError
    N = int(N / 100) * T  # N = number of output samples required
    nnarray = []
    for eachMinor in minorSamples:
        # nnarray all nearest neighbor [[2.4, 2.5, 'a'],[2.3, 2.2, 'a'],[2.5, 2.5, 'a']]
        nnarray = (getNeighbors(dataSet, eachMinor, k))
    populate(N, minorSamples, nnarray, numattrs)



def populate(N, minorSample, nnarray, numattrs):
    """
    perform actual algorithm
    1) take minorsample and nearest neighbors. 
    2) find out difference between attributes of minorsample and nearest neighbors as diff
    3) generate a positive random float number between 0  and 1 known as gap
    4) new attributes of minorsample =  (attributes of minorsample) + gap * difference
    5) As described above, all attribute for a particular sample are generated
    6) such  controlled randomness is added to N number of samples to generate synthetic ones
    
    :param N:  factor by which sample needs to be increase, e.g. 2 means twice
    :param minorSample: all minor samples
    :param nnarray: nearest neighbor array   [[2.4, 2.5, 'a'],[2.3, 2.2, 'a'],[2.5, 2.5, 'a']]
    :param numattrs: equals to number of feature (3) , in 0 based index it iterates from 0,1,2,3
    :return:
    """
    while (N > 0):
        nn = randint(0, len(nnarray) - 2)
        eachUnit = []
        for attr in range(0, numattrs+1): #[0,1,2,3] iterate over each attribute (feature)
            diff = float(nnarray[nn][attr]) - (minorSample[nn][attr]) # difference between nearest neighbor and actual minor sample
            gap = random.uniform(0, 1) # generate a random number between 0 and 1
            eachUnit.append(minorSample[nn][attr] + gap * diff) # multiply difference with random number and add this to original attribute value
        for each in eachUnit:
            syntheticData.write(str(each)+",")
        syntheticData.write("\n")
        N = N - 1



numattrs = 4  # number of features present in dataset
dataSet = loadDataset('iris.csv', numattrs)
MinorClassName = "Iris-virginica"
minorSamples = seperateMinority(dataSet, MinorClassName, classColumnNumber=4)
NumberOfMinorSamples = len(minorSamples)
print "Number Of Minor Samples Present In Dataset : ", NumberOfMinorSamples
SMOTE(NumberOfMinorSamples, 500, minorSamples, numattrs - 1, dataSet, 3)
