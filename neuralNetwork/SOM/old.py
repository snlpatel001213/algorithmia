import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
import scipy.misc
from PIL import Image
import matplotlib

def load_image(infilename):
    """
    will load image from the file
    :param infilename: filename
    :return: numpy array of image
    """
    img = ndimage.imread(infilename)
    data = np.asarray(img, dtype="int32")
    resized = data.reshape(data.shape[2], data.shape[0], data.shape[1])
    return resized


def getRGBForPixel(imageArray, i, j):
    """
    for a particular pixel, it return RGB value
    :param imageArray:
    :param i:
    :param j:
    :return:
    """
    return imageArray[i, j]

def setRGBforPixel(imageArray, i, j , RGBValue):
    """
    for a particular pixel, it set RGB value
    :param imageArray:
    :param i:
    :param j:
    :return: imageArray
    """
    R, G, B = imageArray
    R[i][j] = RGBValue[0]
    G[i][j] = RGBValue[1]
    B[i][j] = RGBValue[2]
    imageArray = [R,G,B]




def findEucledeanDistanceBetweeenLattice(lattice1, lattice2):
    """
    if two point on 2d surface are given, it will return distance between two points
    :param lattice1: list [x,y]
    :param lattice2: list [x1,y1]
    :return:
    """
    return math.sqrt(math.pow(lattice1[0] - lattice2[0], 2) + math.pow(lattice1[1] - lattice2[1], 2))


def makeDummyImage(neighbours, imageArray):
    """
    to make dummy image, just for illustration purpose
    :param neighbours: All neighbours, array of array
    :param imageArray:
    :return:
    """
    height = len(imageArray[0])
    width = len(imageArray[0][0])

    im = [[255 for x in range(height)] for y in range(width)]
    for each in neighbours:
        im[each[0]][each[1]] = 1
    plt.figimage(im)
    plt.show()


def findNeighbours(BMU, Radius, imageArray):
    """
    If best matching unit (BMU) is found, it will find neighbours in given radius
    :param BMU: x y axis for winner node
    :param Radius:
    :param imageArray:
    :return:xml
    """
    height = len(imageArray[0])
    width = len(imageArray[0][0])
    neighbours = []
    for i in range(0, height):
        for j in range(0, width):
            if findEucledeanDistanceBetweeenLattice(BMU, [i, j]) < Radius:
                neighbours.append([i, j])
    return neighbours


def findBMU(inputVectorI, inputVectorJ, imageArray):
    """
    will find best matching unit for given  inputVectorI and inputVectorJ
    :param inputVectorI: x
    :param inputVectorJ: y
    :param imageArray:
    :return: return x1 and y1 coordinates for BMU
    """
    height = len(imageArray[0])
    width = len(imageArray[0][0])
    minDistance = 9999999
    minI = width + 1
    minJ = height + 1
    inputVector = getRGBForPixel(imageArray, inputVectorI, inputVectorJ)
    for i in range(0, height):
        for j in range(0, width):
            R, G, B = getRGBForPixel(imageArray, i, j)
            # print R,G,B
            distance = math.pow(inputVector[0] - R, 2) + math.pow(inputVector[1] - G, 2) + math.pow(inputVector[2] - B,
                                                                                                    2)
            if (distance < minDistance and i != inputVectorI and j != inputVectorJ):
                minI = i
                minJ = j
                minDistance = distance
                break
    return minI, minJ

def decayRadius(initialRadius,timeOrIterations):
    """
    will perform exponential decay of given radius
    :param initialRadius: radius at time t0
    :param timeOrIterations: iteration number
    :return:
    """
    rateOfDecay = 10 # MORE THE RATE MORE WILL BE THE TIME TAKEN, WILL BE EXPLAINED BY GRAPH
    return initialRadius*(math.exp(-timeOrIterations/rateOfDecay))

def decayLearningrate(initialLearningRate,timeOrIterations):
    """
    will perform exponential decay of given radius
    :param initialRadius: radius at time t0
    :param timeOrIterations: iteration number
    :return:
    """
    rateOfDecay = 5 # MORE THE RATE MORE WILL BE THE TIME TAKEN, WILL BE EXPLAINED BY GRAPH
    return initialLearningRate*(math.exp(-timeOrIterations/rateOfDecay))

def updateWeights(weightAtGivenTime,inputVectorWeight,learningRate):
    """
    will update weight and will return new weights, weights are basically RGB color of the image
    :param weightAtGivenTime: RGB
    :param inputVectorWeight: RGB
    :return:
    """
    newWeights = []
    for eachweightNo in range(0,len(weightAtGivenTime)):
        newweight = weightAtGivenTime[eachweightNo] + (learningRate*(inputVectorWeight[eachweightNo]-weightAtGivenTime[eachweightNo]))
        newWeights.append(int(newweight))
    return newWeights

def Main():
    global imageArray
    imageArray = load_image("1.jpg")

    height = len(imageArray[0])  # getting image height
    width = len(imageArray[0][0])  # getting  image width

    # inputvector = [127, 122]  # [127,130] will print bigger
    # print "Input vector is defined at : ", inputvector
    # BMUi, BMUj = findBMU(inputvector[0], inputvector[1], list(imageArray))
    # print "Best matching unit for input vector : ", inputvector, " , found at : ", BMUi, BMUj
    # # distance between two point 1) input vector and 2) BMU is considered as radius
    # radius = findEucledeanDistanceBetweeenLattice(inputvector, [BMUi, BMUj])
    # print "Radius was found to be  : ", radius
    for i in range(0, height):
        for j in range(0, width):
            inputvector = [i, j]
            print inputvector
            BMUi, BMUj = findBMU(inputvector[0], inputvector[1], list(imageArray))
            radius = findEucledeanDistanceBetweeenLattice(inputvector, [BMUi, BMUj])
            initialRadius = radius
            initalLearningRate = 0.2
            iteration = 10
            inputVectorWeight = getRGBForPixel(imageArray, inputvector[0], inputvector[1])
            for iterationNo in range(0, iteration):
                decayedRadius = decayRadius(initialRadius, iterationNo)
                decayedLearningrate = decayLearningrate(initalLearningRate, iterationNo)
                neighbours = findNeighbours([BMUi, BMUj], decayedRadius, imageArray)
                for eachNeighbour in neighbours:
                    R, G, B = getRGBForPixel(imageArray, eachNeighbour[0], eachNeighbour[1])
                    newWeights = updateWeights([R, G, B], inputVectorWeight, decayedLearningrate)
                    setRGBforPixel(imageArray, eachNeighbour[0], eachNeighbour[1], newWeights)
                    # print "So Found Neighbours : ", neighbours
            data = np.asarray(imageArray, dtype="int32")
            # imageArray1 = data.reshape(data.shape[1], data.shape[2], data.shape[0], )
            scipy.misc.toimage(imageArray).save('outfile_with_0.5_as_learningRate' + str(i) + '.jpg')

    data = np.asarray(imageArray, dtype="int32")
    imageArray = data.reshape(data.shape[1], data.shape[2], data.shape[0], )
    scipy.misc.toimage(imageArray).save('Final.jpg')

# Main()
#
# iteration = 100
# # global  imageArray
# imageArray = load_image("RGB_Edition_7.jpg")
# print len(imageArray)
#
# height = len(imageArray[0])  # getting image height
# width = len(imageArray[0][0])  # getting  image width
#
# inputvector = [127,130]  # [127,130] will print bigger
# print "Input vector is defined at : ", inputvector
# BMUi, BMUj = findBMU(inputvector[0], inputvector[1], imageArray)
# print "Best matching unit for input vector : ", inputvector, " , found at : ", BMUi, BMUj
# # distance between two point 1) input vector and 2) BMU is considered as radius
# radius = findEucledeanDistanceBetweeenLattice(inputvector, [BMUi, BMUj])
# print "Radius was found to be  : ", radius
# initialRadius = radius
# initalLearningRate = 0.1
#
# inputVectorWeight = getRGBForPixel(imageArray,inputvector[0],inputvector[1])
# for i in range(0,iteration):
#     decayedRadius = decayRadius(initialRadius,i)
#     decayedLearningrate = decayLearningrate(initalLearningRate,i)
#     neighbours = findNeighbours([BMUi, BMUj], decayedRadius, imageArray)
#     for eachNeighbour in neighbours:
#         R,G,B = getRGBForPixel(imageArray,eachNeighbour[0],eachNeighbour[1])
#         newWeights = updateWeights([R,G,B],inputVectorWeight,decayedLearningrate)
#         imageArray = setRGBforPixel(imageArray, eachNeighbour[0], eachNeighbour[1] , newWeights)
#     print "So Found Neighbours : ", neighbours
#
#
#
# data = np.asarray(imageArray, dtype="int32")
# imageArray = data.reshape(data.shape[1], data.shape[2],data.shape[0])
# scipy.misc.toimage(imageArray).save('outfile_with_0.5_as_learningRate.jpg')

import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
import scipy.misc
from PIL import Image
import matplotlib


im = Image.open("1.jpg")
imageArray = im.load()
global imageArray
inputvector = [127,130]  # [127,130] will print bigger

print inputvector
BMUi, BMUj = findBMU(inputvector[0], inputvector[1], list(imageArray))
radius = findEucledeanDistanceBetweeenLattice(inputvector, [BMUi, BMUj])
initialRadius = radius
initalLearningRate = 0.2
iteration = 10
inputVectorWeight = getRGBForPixel(imageArray, inputvector[0], inputvector[1])

for iterationNo in range(0, iteration):
    decayedRadius = decayRadius(initialRadius, iterationNo)
    decayedLearningrate = decayLearningrate(initalLearningRate, iterationNo)
    neighbours = findNeighbours([BMUi, BMUj], decayedRadius, imageArray)
    print neighbours
    for eachNeighbour in neighbours:
        setRGBforPixel(imageArray, eachNeighbour[0], eachNeighbour[1], [0,0,0])
    break

data = np.asarray(imageArray, dtype="int32")
data = data.reshape(data.shape[1],data.shape[2],data.shape[0])
scipy.misc.toimage(data).save('Final.jpg')