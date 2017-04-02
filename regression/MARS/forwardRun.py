import csv
import math
import traceback


def findTrendline(xArray, yArray):
    """
    used to find trend-line
    :param xArray:  Array with all elements in X
    :param yArray: Array with all elements in Y
    :return:
    """
    # print xArray
    # print yArray
    xAvg = sum(xArray) / len(xArray)
    yAvg = sum(yArray) / len(yArray)
    upperPart = 0
    lowerPart = 0
    m = 0
    # implementing mathematics behind trendline
    for i in range(0, len(xArray)):
        upperPart += (xArray[i] - xAvg) * (yArray[i] - yAvg)
        lowerPart += math.pow(xArray[i] - xAvg, 2)
        m = upperPart / lowerPart
    b = yAvg - m * xAvg
    return m, b

def loadFromcsv(fileName):
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


def findBreakPointsRaw(difference):
    """
    find breakpoints for allocation of different slop (m) and coefficient (b) to each fragment
    :param difference: is the array which shows what is the difference between current point and the same point on trend-line
    :return: subFragments, also referred as brekpoints
    """
    subFragments = []
    # print len(difference)
    lastPoint = 0
    interMediatePoints = []
    for i in range(1, len(difference) - 1):
        interMediatePoints.append(i)
        if difference[i - 1] > difference[i] < difference[i + 1]:
            # if i lower than i-1 and i+1 it will be defined as breakpoint
            # this will be a crest in local region \/

            lastPoint = i
            subFragments.append(interMediatePoints)
            interMediatePoints = []
            # print "low Diffrernce point Identified", i + 1
        if difference[i - 1] < difference[i] > difference[i + 1]:
            # if i higher than i-1 and i+1 it will be defined as breakpoint
            # this will be a trough in local region /\

            lastPoint = i
            subFragments.append(interMediatePoints)
            interMediatePoints = []
            # print "High Diffrernce point Identified", i + 1

    # processing last fragment
    subFragments.append([j for j in range(lastPoint + 1, len(difference) + 1)])
    return subFragments


def findBreakPointsAdvance(difference):
    """
    find breakpoints for allocation of different slop and b0 to each fragment
    :param difference: is the array which shows what is the difference between current point and the same point on trend-line
    :return: subFragments, also referred as brekpoints
    """
    subFragments = []

    lastPoint = 0
    interMediatePoints = []
    for i in range(1, len(difference) - 1):
        interMediatePoints.append(i)

        # percentageDifferenceBetweenThreePoints - it measures, what is percentage difference between i and i-1 and i+1 point
        percentageDifferenceBetweenThreePoints = difference[i] * 10 / (difference[i - 1] + difference[i + 1]) / 2

        # application of some more conditions in below given function will avoid formation of segments containing only one point
        if (difference[i - 1] > difference[i] < difference[i + 1]) and percentageDifferenceBetweenThreePoints < 50:
            # if i lower than i-1 and i+1 it will be defined as breakpoint
            # with additional condition the difference must be lesser than 50%
            # this will be a crest in local region \/
            lastPoint = i
            subFragments.append(interMediatePoints)
            interMediatePoints = []
            # print "low Diffrernce point Identified", i + 1
        if (difference[i - 1] < difference[i] > difference[i + 1]) and percentageDifferenceBetweenThreePoints > 150:
            # if i higher than i-1 and i+1 it will be defined as breakpoint
            # with additional condition the difference must be lesser than 150%
            # this will be a trough in local region /\
            lastPoint = i
            subFragments.append(interMediatePoints)
            interMediatePoints = []
            # print "High Diffrernce point Identified", i + 1

    # processing last fragment
    subFragments.append([j for j in range(lastPoint + 1, len(difference) + 1)])
    return subFragments





def fragmentCombiner(breakPoints, slopAndCoefficientArray):
    """
        combine smaller fragments to bigger one

    :param breakPoints: all breakpoints [[1,2,3],[4,5,6,7],...[..][..]]
    :param slopAndCoefficientArray: slop and regression coefficient for all fragments
    e.g.[[.06,6.4],[.76,3.4]] where .06 is the slop & 6.4 is the regression coefficient
    :return:
    """
    newForwardArray = [] # to store fragments after merger of one or many fragments
    for i in range(0, len(breakPoints) - 2, 2):

        slopAndCoefficientCurrent = slopAndCoefficientArray[i] # coefficient of current fragment
        slopAndCoefficientNext = slopAndCoefficientArray[i + 1] # coefficient of Next fragment

        # percentage difference between coefficient of current and next fragment
        percentageDiff = slopAndCoefficientNext[1] * 100 / slopAndCoefficientCurrent[1]

        """
        if percentage difference between coefficient is between 20 then combine.
        """
        if (percentageDiff < 20 or percentageDiff > -20) :
            temp1 = []
            # if this condition is satisfied then two fragments will be merged in to one
            temp1.extend(breakPoints[i])
            temp1.extend(breakPoints[i + 1])
            # new array with less number of fragments
            newForwardArray.append(temp1)

    return newForwardArray

def withForwardRun():
    """
    This function implements Multivariate adaptive regression splines with forward run
    In short all fragment wgich can be combined with out significant loss in accuracy can will be combined as bigger fragmnets
    :return:
    """
    # loading  data-set
    # https://datamarket.com/data/set/22s2/annual-swedish-fertility-rates-1000s-1750-1849-thomas-1940#!ds=22s2&display=line
    # Annual Swedish fertility rates (1000's) 1750-1849 Thomas (1940)

    # loading  dataset
    array = loadFromcsv("SwidishFertility")
    # loded dataset in previous step is in string form, converting to float
    array = convertDataToFloat(array)
    xArray = []
    yArray = []

    # Seperating data in to x and y
    for eachXYPAir in array:
        x = eachXYPAir[0]
        y = eachXYPAir[1]
        xArray.append(x)
        yArray.append(y)

    # getting trend line for the entire data
    m, b = findTrendline(xArray, yArray)

    difference = []  # will store difference between actual value of y and Ytrend (y derieved from trendline)
    yArray = []

    for eachXYPAir in array:
        x = eachXYPAir[0]
        y = eachXYPAir[1]
        Ytrend = m * x + b  # finding derived value of Y called as Ytrend (y derieved from trendline) from so found m and b in previous code block
        yArray.append(y)
        difference.append(abs(y - Ytrend))
    """
        Breakpoints here are the point which separates group of data having similar slop, locally called fragments
    """
    breakPoints = findBreakPointsAdvance(difference)
    # print breakPoints

    # below given code fragment will give slop and coefficient, for each fragment.
    slopAndCoefficientArray = []  # m = slop and b = regression coefficient
    for eachFragment in breakPoints:
        # print eachFragment,
        xFragment = xArray[eachFragment[0] - 1:eachFragment[-1]]
        yFragment = yArray[eachFragment[0] - 1:eachFragment[-1]]
        m, b = findTrendline(xFragment, yFragment)
        slopAndCoefficientArray.append([m, b])

    # print slopAndCoefficientArray # having m = slop and b = regression coefficient for each fragment

    # differenceArray = fragmentCombiner(breakPoints, slopAndCoefficientArray)
    # print differenceArray

    # Fragment combiner is a function that combines relavant fragment on preset criteria
    # Will explore the function in detail soon
    # intially the fragment number was 35, now decreased to 17, after application of  fragmentCombiner function.
    breakPoints = fragmentCombiner(breakPoints, slopAndCoefficientArray)
    # print breakPoints

    for eachFragment in breakPoints:
        # print eachFragment,

        # Getting x and y for the given Fragment range
        xFragment = xArray[eachFragment[0] - 1:eachFragment[-1]]
        yFragment = yArray[eachFragment[0] - 1:eachFragment[-1]]

        # finding trendline for the given Fragment range
        m, b = findTrendline(xFragment, yFragment)
        # print m,b

        # Getting x and y for the given Fragment range
        xValueForFragment = [xArray[j - 1] for j in range(eachFragment[0], eachFragment[-1] + 1)]
        yValueForFragment = [yArray[j - 1] for j in range(eachFragment[0], eachFragment[-1] + 1)]
        yDerived = [xArray[j - 1] * m + b for j in range(eachFragment[0], eachFragment[-1] + 1)]

        # printing value of y and yTrend for printing
        for i in range(0, len(xValueForFragment)):
            print yValueForFragment[i], yDerived[i]
        print ""


withForwardRun()