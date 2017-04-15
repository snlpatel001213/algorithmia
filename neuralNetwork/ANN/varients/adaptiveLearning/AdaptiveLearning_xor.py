import math

"""
defining XOR gate, [x1, x2 , y]
"""
XOR = [[0, 1, 1], [1, 1, 0], [1, 0, 1], [0, 0, 0]]

# initializing weights
w13 = 0.5
w14 = 0.9
w23 = 0.4
w24 = 1.0
w35 = -1.2
w45 = 1.1
t3 = 0.8
t4 = -0.1
t5 = 0.3
# defining learning rate
alpha = 0.5
# initializing squaredError
squaredError = 0
# initializing error per case
error = 0
# defining epochs
Epochs = 2000
count = 0
# run this repeatedly for number of Epochs
global slopArray  # to store slops
slopArray = []


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


def changeAdaptively(squaredErrorArray, EpochArray, alpha):
    """
    to change learning rate(alpha) adaptively
    :param squaredErrorArray:  Array containing squared error for all completed epochs: [1.2340,0.1,0.45,0.85,0.4,0.4430,0.3244]
    :param EpochArray: Array containing all completed epochs: [1,2,3,4,5,....50,51.]
    :param alpha: [current learning rate]
    :return:
    """
    # print "went ti this func"
    # print squaredErrorArray[-10:],EpochArray[-10:]
    m, b = findTrendline(squaredErrorArray[-10:], EpochArray[-10:]) # find slop for current lat 10 error value
    try:
        if m > slopArray[-1]: #slopArray[-1] previous slop, m current slop
            """
                If present slop is greater than previous one, it indicates decrease in error gradually
                This usually happens at beginning and middle of learning process
                then increase learning rate further to decelerate error further

            """
            slopArray.append(m)
            newAlpha = alpha * 1.08
        else:
            """
            If present slop is less than previous, it indicates instability or very less chane  in error
            this usually happens near to convergence point.
            then decrease learning rate
            """
            slopArray.append(m)
            newAlpha = alpha / 1.04
        return newAlpha
    except:
        # for first iteration when nothing will be there in slopArray
        # so slop will throw exception and will be handled by except block
        slopArray.append(m)
        return alpha

def Main():
    EpochArray = []
    squaredErrorArray = []
    for j in range(Epochs):
        # printing squaredError, alpha after each epoch
        print"squaredError", squaredError, alpha
        # making update to learning rate after every 10 epochs
        if j % 10 == 0 and j != 0:
            alpha = changeAdaptively(squaredErrorArray, EpochArray, alpha)
        # appending squared error to squaredErrorArray
        squaredErrorArray.append(squaredError)
        # appending number of completed epochs to EpochArray
        EpochArray.append(j)
        squaredError = 0
        for i in range(4):  # iterating through each case for given iteration

            """
            calculating output at each perceptron
            """
            y3 = 1 / (1 + math.exp(-((XOR[i][0] * w13) + (XOR[i][1] * w23 - t3))))
            y4 = 1 / (1 + math.exp(-(XOR[i][0] * w14 + XOR[i][1] * w24 - t4)))
            y5 = 1 / (1 + math.exp(-(y3 * w35 + y4 * w45 - t5)))
            """
            calculating error
            """
            error = XOR[i][2] - y5

            """
            calculating partial error and change in weight for output and hidden perceptron
            """
            del5 = y5 * (1 - y5) * error
            dw35 = alpha * y3 * del5
            dw45 = alpha * y4 * del5
            dt5 = alpha * (-1) * del5

            """
                calculating partial error and change in weight for input and hidden perceptron
            """

            del3 = y3 * (1 - y3) * del5 * w35
            del4 = y4 * (1 - y4) * del5 * w45
            dw13 = alpha * XOR[i][0] * del3
            dw23 = alpha * XOR[i][1] * del3
            dt3 = alpha * (-1) * del3
            dw14 = alpha * XOR[i][0] * del4
            dw24 = alpha * XOR[i][1] * del4
            dt4 = alpha * (-1) * del4
            """
            calculating weight and bias update
            """
            w13 = w13 + dw13
            w14 = w14 + dw14
            w23 = w23 + dw23
            w24 = w24 + dw24
            w35 = w35 + dw35
            w45 = w45 + dw45
            t3 = t3 + dt3
            t4 = t4 + dt4
            t5 = t5 + dt5

            """
            Since y5 will be in float number between (0 - 1)
            Here we have used 0.5 as threshold, if output is above 0.5 then class will be 1 else 0
            """
            if y5 < 0.5:
                class_ = 0
            else:
                class_ = 1
            """
            uncomment below line to see predicted and actual output
            """
            # print ("Predicted",class_," actual ",XOR[i][2])
            """
            calculating squared error
            """
            squaredError = squaredError + (error * error)
            if squaredError < 0.001:
                # if error is below   0.001, terminate training (premature termination)
                break

Main()
