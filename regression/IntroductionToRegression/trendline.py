import math
def findTrendline(xArray,yArray):
    """
    used to find trend line
    Need certain changes in input
    :param XY:
    :return:
    """
    print xArray
    print yArray
    # calculating average for X
    xAvg = float(sum(xArray)) / len(xArray)

    # calculating average for Y
    yAvg = float(sum(yArray)) / len(yArray)

    upperPart = 0.0 # initializing numerator of the slop equation
    lowerPart = 0.0 # initializing denominator of the slop equation

    m = 0.0 # initializing slop
    for i in range(0, len(xArray)):
        #calculating numerator
        upperPart += (xArray[i] - xAvg) * (yArray[i] - yAvg)
        #calculating denominator
        lowerPart += math.pow(xArray[i] - xAvg,2)

    # calculating slop
    m = upperPart / lowerPart
    # calculating regression coefficient
    b = yAvg - m * xAvg
    return m, b



# Example
x = [183800,183200,174900,173500,172900,173200,173200,169700,174500,177900,188100,203200,230200,258200,309800,329800]
y = [10.30,10.30,10.10,9.30,8.40,7.30,8.40,7.90,7.60,7.60,6.90,7.40,8.10,7.00,6.50,5.80]

print findTrendline(x,y)