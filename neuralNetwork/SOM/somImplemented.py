import math

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy import ndimage


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


def PIL2array(img):
    return np.array(img.getdata(),
                    np.uint8).reshape(3, img.size[1], img.size[0])


def setRGBforPixel(imageData, i, j, RGBValue):
    """
    for a particular pixel, it set RGB value
    :param imageArray:
    :param i:
    :param j:
    :return: imageArray
    """
    imageData[i, j] = tuple(RGBValue)
    return imageData


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


def findNeighbours(BMU, Radius, imageData, imageObject):
    """
    If best matching unit (BMU) is found, it will find neighbours in given radius
    :param BMU: x y axis for winner node
    :param Radius:
    :param imageArray:
    :return:xml
    """
    width = imageObject.size[0]
    height = imageObject.size[1]
    neighbours = []
    for i in range(0, height):
        for j in range(0, width):
            if findEucledeanDistanceBetweeenLattice(BMU, [i, j]) < Radius:
                neighbours.append([i, j])
    return neighbours


def findBMU(inputVectorI, inputVectorJ, imageData, imageObject):
    """
    will find best matching unit for given  inputVectorI and inputVectorJ
    :param inputVectorI: x
    :param inputVectorJ: y
    :param imageArray:
    :return: return x1 and y1 coordinates for BMU
    """
    imageDataArray = PIL2array(imageObject)
    # print imageData, imageObject.size

    minDistance = 9999999
    width = imageObject.size[0]
    height = imageObject.size[1]
    minI = width + 1
    minJ = height + 1
    inputVector = getRGBForPixel(imageData, inputVectorI, inputVectorJ)
    for i in range(0, height):
        for j in range(0, width):
            R, G, B = getRGBForPixel(imageData, i, j)
            # print R,G,B
            distance = math.pow(inputVector[0] - R, 2) + math.pow(inputVector[1] - G, 2) + math.pow(inputVector[2] - B,
                                                                                                    2)
            if (distance < minDistance and i != inputVectorI and j != inputVectorJ):
                minI = i
                minJ = j
                minDistance = distance
                break
    return minI, minJ


def decayRadius(initialRadius, timeOrIterations):
    """
    will perform exponential decay of given radius
    :param initialRadius: radius at time t0
    :param timeOrIterations: iteration number
    :return:
    """
    rateOfDecay = 5  # MORE THE RATE MORE WILL BE THE TIME TAKEN, WILL BE EXPLAINED BY GRAPH
    return initialRadius * (math.exp(-timeOrIterations / rateOfDecay))


def decayLearningrate(initialLearningRate, timeOrIterations):
    """
    will perform exponential decay of given radius
    :param initialRadius: radius at time t0
    :param timeOrIterations: iteration number
    :return:
    """
    rateOfDecay = 5 # MORE THE RATE MORE WILL BE THE TIME TAKEN, WILL BE EXPLAINED BY GRAPH
    return initialLearningRate * (math.exp(-timeOrIterations / rateOfDecay))


def updateWeights(weightAtGivenTime, inputVectorWeight, learningRate):
    """
    will update weight and will return new weights, weights are basically RGB color of the image
    :param weightAtGivenTime: RGB
    :param inputVectorWeight: RGB
    :return:
    """
    newWeights = []
    for eachweightNo in range(0, len(weightAtGivenTime)):
        newweight = weightAtGivenTime[eachweightNo] + (
            learningRate * (inputVectorWeight[eachweightNo] - weightAtGivenTime[eachweightNo]))
        newWeights.append(int(newweight))
    return newWeights

def primaryCode():
    """
    this is for initial illustration, how SOM works
    :return:
    """
    global imageObject
    global imageData
    imageObject = Image.open("1.jpg")
    imageData = imageObject.load()
    print imageObject.size
    inputvector = [180, 80]  # [127,130] will print bigger
    print inputvector
    BMUi, BMUj = findBMU(inputvector[0], inputvector[1], imageData, imageObject)
    radius = findEucledeanDistanceBetweeenLattice(inputvector, [BMUi, BMUj])
    print radius, BMUi, BMUj

    initialRadius = radius
    initalLearningRate = 0.2
    iteration = 10
    inputVectorWeight = getRGBForPixel(imageData, inputvector[0], inputvector[1])
    for iterationNo in range(0, 100):
        decayedRadius = decayRadius(initialRadius, iterationNo)
        decayedLearningrate = decayLearningrate(initalLearningRate, iterationNo)
        neighbours = findNeighbours([BMUi, BMUj], decayedRadius, imageData, imageObject)
        print neighbours
        for eachNeighbour in neighbours:
            R, G, B = getRGBForPixel(imageData, eachNeighbour[0], eachNeighbour[1])
            newWeights = updateWeights([R, G, B], inputVectorWeight, decayedLearningrate)
            setRGBforPixel(imageData, eachNeighbour[0], eachNeighbour[1], newWeights)
        imageObject.save("img1.jpg")


def perfectlyWorkingCode():
    """
    this code is perfectly working
    :return:
    """
    global imageObject
    global imageData
    imageObject = Image.open("RGB_Edition_7.jpg")
    imageData = imageObject.load()

    print imageObject.size
    width = imageObject.size[0]
    height = imageObject.size[1]
    for i in range(0, height):
        for j in range(0, width):
            inputvector = [i, j]  # [127,130] will print bigger
            print inputvector
            # print radius, BMUi, BMUj
            BMUi, BMUj = findBMU(inputvector[0], inputvector[1], imageData, imageObject)
            radius = findEucledeanDistanceBetweeenLattice(inputvector, [BMUi, BMUj])
            initialRadius = radius
            initalLearningRate = 0.2
            iteration = 10
            inputVectorWeight = getRGBForPixel(imageData, inputvector[0], inputvector[1])
            for iterationNo in range(0, iteration):
                decayedRadius = decayRadius(initialRadius, iterationNo)
                decayedLearningrate = decayLearningrate(initalLearningRate, iterationNo)
                if decayedRadius > 10:
                    decayedRadius = 5
                    neighbours = findNeighbours([BMUi, BMUj], decayedRadius, imageData, imageObject)
                else:
                    neighbours = findNeighbours([BMUi, BMUj], decayedRadius, imageData, imageObject)
                # print neighbours
                for eachNeighbour in neighbours:
                    R, G, B = getRGBForPixel(imageData, eachNeighbour[0], eachNeighbour[1])
                    newWeights = updateWeights([R, G, B], inputVectorWeight, decayedLearningrate)
                    setRGBforPixel(imageData, eachNeighbour[0], eachNeighbour[1], newWeights)
            imageObject.save("img1.jpg")



# lets take each file
global imageObject
global imageData
imageObject = Image.open("RGB_Edition_7.jpg")
imageData = imageObject.load()

print imageObject.size
width = imageObject.size[0]
height = imageObject.size[1]
counter = 0
for i in range(0, height):
    for j in range(0, width):
        inputvector = [i, j]  # [127,130] will print bigger
        print inputvector
        # print radius, BMUi, BMUj
        BMUi, BMUj = findBMU(inputvector[0], inputvector[1], imageData, imageObject)
        radius = findEucledeanDistanceBetweeenLattice(inputvector, [BMUi, BMUj])
        initialRadius = radius
        initalLearningRate = 0.2
        iteration = 10
        inputVectorWeight = getRGBForPixel(imageData, inputvector[0], inputvector[1])
        for iterationNo in range(0, iteration):
            decayedRadius = decayRadius(initialRadius, iterationNo)
            decayedLearningrate = decayLearningrate(initalLearningRate, iterationNo)
            if decayedRadius > 10:
                decayedRadius = 5
                neighbours = findNeighbours([BMUi, BMUj], decayedRadius, imageData, imageObject)
            else:
                neighbours = findNeighbours([BMUi, BMUj], decayedRadius, imageData, imageObject)
            # print neighbours
            for eachNeighbour in neighbours:
                R, G, B = getRGBForPixel(imageData, eachNeighbour[0], eachNeighbour[1])
                newWeights = updateWeights([R, G, B], inputVectorWeight, decayedLearningrate)
                setRGBforPixel(imageData, eachNeighbour[0], eachNeighbour[1], newWeights)
        if counter%100 == 0:
            imageObject.save("image/"+str(counter)+".jpg")
        counter = counter+1