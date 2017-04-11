import math
import random

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
for j in range(2000):
    print"squaredError", squaredError
    # initializing squaredError per epoch
    squaredError = 0
    for i in range(4): # iterating through each case for given iteration
        y3 = 1 / (1 + math.exp(-((XOR[i][0] * w13) + (XOR[i][1] * w23))))
        y4 = 1 / (1 + math.exp(-(XOR[i][0] * w14 + XOR[i][1] * w24)))
        y5 = 1 / (1 + math.exp(-(y3 * w35 + y4 * w45)))
        error = XOR[i][2] - y5

        del5 = y5 * (1 - y5) * error
        dw35 = alpha * y3 * del5
        dw45 = alpha * y4 * del5
        dt5 = alpha * (-1) * del5

        del3 = y3 * (1 - y3) * del5 * w35
        del4 = y4 * (1 - y4) * del5 * w45

        # CHANGES BETWEEN INPUT AND MIDDLE LAYER
        dw13 = alpha * XOR[i][0] * del3
        dw23 = alpha * XOR[i][1] * del3
        dt3 = alpha * (-1) * del3
        dw14 = alpha * XOR[i][0] * del4
        dw24 = alpha * XOR[i][1] * del4
        dt4 = alpha * (-1) * del4
        # print (">>>>>>>>>>>>>>",del4,del3,del5)
        # corrections
        w13 = w13 + dw13
        w14 = w14 + dw14
        w23 = w23 + dw23
        w24 = w24 + dw24
        w35 = w35 + dw35
        w45 = w45 + dw45
        t3 = t3 + dt3
        t4 = t4 + dt4
        t5 = t5 + dt5
        if y5 < 0.5:
            temporary = 0
        else:
            temporary = 1

        # print (">>",XOR[i][0],XOR[i][1],">>",temporary," actual ",XOR[i][2])
        # print (">>>>>",error*error)
        squaredError = squaredError + (error * error)
        if squaredError < 0.001:
            break
