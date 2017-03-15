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


def fragmentCombiner(breakPoints, slopAndCoefficientArray):
    """
    combine smaller fragments to bigger one
    :return:
    """
    newForwardArray = []
    for i in range(0, len(breakPoints) - 2, 2):
        # print breakPoints[i]

        # taking slop as well as coefficient for current fragment as well as next fragment in current fragment
        slopAndCoefficientCurrent = slopAndCoefficientArray[i]
        slopAndCoefficientNext = slopAndCoefficientArray[i + 1]

        # slopAndCoefficientNext[1] - slop for next element,slopAndCoefficientCurrent[1] - slop for current element
        # slopAndCoefficientNext[0] - coefficient for next element,slopAndCoefficientCurrent[0] - coefficient for current element
        # percentageDiff is difference in percentage between two adjacent slops
        # simply if slop and coefficient and range , combine two adjacent fragments

        percentageDiff = slopAndCoefficientNext[1] * 100 / slopAndCoefficientCurrent[1]
        if (percentageDiff < 20 or percentageDiff > -20) and (
                            slopAndCoefficientCurrent[0] - slopAndCoefficientCurrent[1] < 15 or
                            slopAndCoefficientCurrent[0] -
                            slopAndCoefficientCurrent[1] > -15):
            temp1 = []
            temp1.extend(breakPoints[i])
            temp1.extend(breakPoints[i + 1])
            newForwardArray.append(temp1)
            # print newForwardArray # you may print this if required

    return newForwardArray


def withoutForwardRun():
    """
    This function only finds trendline and shows trendline for each fragment
    this is without forward run, where many small fragment exists
    :return:
    """

    # loading  data-set
    # https://datamarket.com/data/set/22s2/annual-swedish-fertility-rates-1000s-1750-1849-thomas-1940#!ds=22s2&display=line
    # Annual Swedish fertility rates (1000's) 1750-1849 Thomas (1940)

    array = loadFromcsv("SwidishFertility")
    # loded dataset in previous step is in string form, converting to float
    array = convertDataToFloat(array)
    xArray = []
    yArray = []

    # separating data in to X and Y
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
        # print y , Ytrend , abs(y-Ytrend) # lets print and see how we will define breakpoints here
        """
        Breakpoints here are the point which separates group of data having similar slop, locally called fragments
        """
    # breakPoints = findBreakPointsRaw( difference) # define breakpoint using findBreakPointsRaw function
    breakPoints = findBreakPointsAdvance(difference)  # define breakpoint using findBreakPointsAdvance function

    # will print breakPoints
    # below given block is for printing purpose only, You may comment this down if you don't need it
    # print breakPoints
    # for each in breakPoints:
    #     for i in each:
    #         print yArray[i]
    #     print ""

    # finding slop and regression coefficient for each Fragment between breakPoint
    for eachFragment in breakPoints:
        # print eachFragment,

        # Getting x and y for the given Fragment range
        xFragment = xArray[eachFragment[0] - 1:eachFragment[-1]]
        yFragment = yArray[eachFragment[0] - 1:eachFragment[-1]]

        # finding trendline for the given Fragment range
        m, b = findTrendline(xFragment, yFragment)

        # Getting x and y for the given Fragment range
        xValueForFragment = [xArray[j - 1] for j in range(eachFragment[0], eachFragment[-1] + 1)]
        yValueForFragment = [yArray[j - 1] for j in range(eachFragment[0], eachFragment[-1] + 1)]

        # Getting yTrend for the given Fragment range
        yDerived = [xArray[j - 1] * m + b for j in range(eachFragment[0], eachFragment[-1] + 1)]

        # printing value of y and yTrend for printing
        for i in range(0, len(xValueForFragment)):
            print yValueForFragment[i], yDerived[i]
        print ""


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


    l = 0
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
        l = l + 1

withoutForwardRun()