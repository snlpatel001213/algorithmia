import math


def findTrendline(xArray, yArray):
    """
    used to find trend line
    Need certain changes in input
    :param XY:
    :return:
    """
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


def findBreakPoints(difference):
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


def simpleMARS(inputData):
    """
    This function only finds trend-line and shows trendline for each fragment
    this is without forward run, where many small fragment exists
    :return:
    """
    xArray = []
    yArray = []

    # separating data in to X and Y
    """
    if data is something like [[1,0],[2,5],[3,6],[8,7],[10,8]]
    then xArray and yArray would look like this
    xArray = [1,2,3,8,10]
    yArray = [0,5,6,7,8]
    """
    for eachXYPAir in inputData:
        x = eachXYPAir[0]
        y = eachXYPAir[1]
        xArray.append(x)
        yArray.append(y)
    # getting trend line for the entire data
    m, b = findTrendline(xArray, yArray)

    difference = []  # will store difference between actual value of y and Ytrend (y derieved from trendline)
    yArray = []

    for eachXYPAir in inputData:
        # separating data in to X and Y
        x = eachXYPAir[0]
        y = eachXYPAir[1]
        # getting Ypredict using previously calculated b and m.
        # Ytrend will be the trend-line as shown in graph
        Ytrend = m * x + b  # finding derived value of Y called as Ytrend (y derieved from trendline) from so found m and b in previous code block
        yArray.append(y)
        # difference are differences between Ytrend and Yactual points in YArray
        difference.append(abs(y - Ytrend))
        # print y , Ytrend , abs(y-Ytrend) # lets print and see how we will define breakpoints here
        """
        Breakpoints here are the point which separates group of data having similar slop, locally called fragments
        """
    # breakPoints = findBreakPointsRaw( difference) # define breakpoint using findBreakPointsRaw function
    breakPoints = findBreakPoints(difference)  # define breakpoint using findBreakPointsAdvance function

    for eachFragment in breakPoints:
        # print eachFragment,

        # Getting x and y for the given Fragment range
        xFragment = xArray[eachFragment[0] - 1:eachFragment[-1]]
        yFragment = yArray[eachFragment[0] - 1:eachFragment[-1]]

        # finding trendline for the given Fragment range
        m, b = findTrendline(xFragment, yFragment)

        # Getting yTrend for the given Fragment range
        yDerived = [xArray[j - 1] * m + b for j in range(eachFragment[0], eachFragment[-1] + 1)]

        # printing value of y and yTrend for printing
        for i in range(0, len(xFragment)):
            print yFragment[i], yDerived[i]
        print ""


inputData = [[1, 42],
         [2, 41.5],
         [3, 41],
         [4, 40.5],
         [5, 40],
         [6, 39.5],
         [7, 39],
         [8, 38.5],
         [9, 38],
         [10, 37.5],
         [11, 37],
         [12, 36.5],
         [13, 36],
         [14, 35.5],
         [15, 35],
         [16, 34.5],
         [17, 34],
         [18, 33.5],
         [19, 33],
         [20, 32.5],
         [21, 32],
         [22, 31.5],
         [23, 31],
         [24, 30.5],
         [25, 30],
         [26, 31.5],
         [27, 33],
         [28, 34.5],
         [29, 36],
         [30, 37.5],
         [31, 39],
         [32, 40.5],
         [33, 42],
         [34, 43.5],
         [35, 45],
         [36, 46.5],
         [37, 48],
         [38, 49.5],
         [39, 51],
         [40, 52.5],
         [41, 54],
         [42, 55.5],
         [43, 57],
         [44, 58.5],
         [45, 60],
         [46, 61.5],
         [47, 63],
         [48, 64.5],
         [49, 66],
         [50, 67.5]]

simpleMARS(array)
