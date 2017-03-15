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
    e.g. https://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data
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
    print xArray
    print yArray
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

def findBreakPoints(Yarray, difference):
    """
    find breakpoints for allocation of different slop and b0 to each fragment
    :param Yarray:
    :param difference:
    :return:
    """
    subGraphPart = []
    # print Yarray,difference
    print len(difference)
    lastPoint = 0
    interMediatePoints = []
    for i in range(1, len(difference) - 1):
        interMediatePoints.append(i)
        if difference[i - 1] > difference[i] < difference[i + 1]:
            # interMediatePoints.append(i)
            lastPoint = i
            subGraphPart.append(interMediatePoints)
            interMediatePoints = []
            print "low Diffrernce point Identified", i + 1
        if difference[i - 1] < difference[i] > difference[i + 1]:
            lastPoint = i
            # interMediatePoints.append(i)
            subGraphPart.append(interMediatePoints)
            interMediatePoints = []
            print "High Diffrernce point Identified", i + 1
    # processing last part
    subGraphPart.append([j for j in range(lastPoint + 1, len(difference)+1)])
    return subGraphPart


array  = loadFromcsv("SwidishFertility")
array  = convertDataToFloat(array)
print array
xArray = []
yArray = []
for eachXYPAir in array:
    x = eachXYPAir[0]
    y = eachXYPAir[1]
    xArray.append(x)
    yArray.append(y)
m, b = findTrendline(xArray,yArray)

difference = []
yArray = []

for eachXYPAir in array:
    x = eachXYPAir[0]
    y = eachXYPAir[1]
    Ytrend = m * x + b
    yArray.append(y)
    difference.append(abs(y - Ytrend))
    # print y , Ytrend , abs(y-Ytrend)
breakPoints = findBreakPoints(yArray, difference)
print breakPoints
for each in breakPoints:
    for i in each:
        print yArray[i]
    print ""

# finding slop and regression coefficient for each slop
# for eachFragment in breakPoints:
#     print eachFragment
#     xFragment = xArray[eachFragment[0]:eachFragment[-1]]
#     yFragment = yArray[eachFragment[0]:eachFragment[-1]]
#     # print eachFragment[0],eachFragment[-1],findTrendline(xFragment,yFragment)
#     #plottting
#     m,b = findTrendline(xFragment, yFragment)
#     xValueForFragment =  [xArray[j-1] for j in range(eachFragment[0], eachFragment[-1]+1)]
#     yValueForFragment = [yArray[j - 1] for j in range(eachFragment[0], eachFragment[-1] + 1)]
#     yDerived  = [xArray[j - 1]*m + b for j in range(eachFragment[0], eachFragment[-1] + 1)]
#     # print xValueForFragment,yValueForFragment, yDerived
#     for i in range (0,len(xValueForFragment)):
#         print xValueForFragment[i],yValueForFragment[i], yDerived[i]
#     print ""

