import math
import csv
import traceback
import matplotlib.pyplot as plt


def loadFromcsv( fileName):
    """
    load a file and conver to 2d python list and return it
    :param fileName: csv file name with absolute path

    Example file  - pima-indians-diabetes.data
    Test the script using following code
    loadDataInstance =  loadData()
    print loadDataInstance.loadFromcsv('pima-indians-diabetes.data')
    :return: 2D arrat [list of [list]]
    e.g. [['6', '148', '72', '35', '0', '33.6', '0.627', '50', '1'], ['1', '85', '66',...]..[]...]
    """
    try:
        data = list(csv.reader(open(fileName)))
        return data
    except:
        return (traceback.print_exc())


def convertDataToFloat(dataset):
    """
    loadFromcsv function returns data as list of list of  strings,
    It must be converted to floats for further processing
    code can be tested through below given snippet

    loadDataInstance = loadData()
    dataset = loadDataInstance.loadFromcsv('pima-indians-diabetes.data')
    print loadDataInstance.convertDataToFloat(dataset)

    :param dataset:
    :return: dataset in floats
    """
    for row in dataset:
        for i in range(len(row)):
            row[i] = float(row[i])
    return dataset


def findTrendline(xArray,yArray):
    """
    used to find trend line
    Need certain changes in input
    :param XY:
    :return:
    """
    print "xArray ;",xArray
    print "yArray :",yArray
    xAvg = sum(xArray) / len(xArray)
    yAvg = sum(yArray) / len(yArray)
    upperPart = 0
    lowerPart = 0
    m = 0
    for i in range(0, len(xArray)):
        upperPart += (xArray[i] - xAvg) * (yArray[i] - yAvg)
        lowerPart += math.pow(xArray[i] - xAvg, 2)
        m = upperPart / lowerPart
    b = yAvg - m * xAvg
    return m, b

def findBreakPoints(yArray, difference):
    """
    find breakpoints for allocation of different slop (m) and coefficient (b) to each fragment
    :param difference: is the array which shows what is the difference between current point and the same point on trend-line
    :return: subFragments, also referred as brekpoints
    """
    subFragments = []
    # print len(difference)
    lastPoint = 0
    interMediatePoints = []
    for i in range(1, len(difference) - 1): # iterating through array having difference between trend-line and actual points
        interMediatePoints.append(i)
        if difference[i - 1] > difference[i] < difference[i + 1]:
            """if difference at given point i is lesser than its surrounding points : [i+1] and [i-1] ,  it will be defined as breakpoint
            this will be a crest in local region \/ """
            lastPoint = i
            subFragments.append(interMediatePoints)
            interMediatePoints = []
            # print "low Diffrernce point Identified", i + 1
        if difference[i - 1] < difference[i] > difference[i + 1]:
            """if difference at given point i is higher than its surrounding points:  : [i+1] and [i-1],  it will be defined as breakpoint
                this will be a crest in local region \/ """
            lastPoint = i
            subFragments.append(interMediatePoints)
            interMediatePoints = []
            # print "High Difference point Identified", i + 1

    # processing last fragment
    subFragments.append([j for j in range(lastPoint + 1, len(difference) + 1)])
    return subFragments


# loading file
dataset  = loadFromcsv("SwidishFertility")
# converting strings to float
dataset  = convertDataToFloat(dataset)
# print dataset
xArray = []
yArray = []

#seperating X and Y from the dataset
for eachXYPAir in dataset:
    x = eachXYPAir[0]
    y = eachXYPAir[1]
    xArray.append(x)
    yArray.append(y)
# finding  trendline   for entire data
m, b = findTrendline(xArray,yArray)

difference = []
yArray = []

for eachXYPAir in dataset:
    x = eachXYPAir[0]
    y = eachXYPAir[1]
    # finding Ypredicted, by using Y and Ypredicted
    Ypredicted = m * x + b
    yArray.append(y)
    difference.append(abs(y - Ypredicted))
    # print y , Ytrend , abs(y-Ytrend)
# finding breakpoints by using difference and Yactual(YArray)
breakPoints = findBreakPoints(yArray, difference)

# print breakPoints

# printing out for plotting in microsoft excel
for each in breakPoints:
    for i in each:
        print yArray[i]
    print "" # will keep space between different fragments

