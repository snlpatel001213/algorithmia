import math
import matplotlib.pyplot as plt
import numpy as np
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
    return resized / 255.0

def PIL2array(img):
    return np.array(img.getdata(),
                    np.uint8).reshape(3,img.size[1], img.size[0])

def getRGBForPixel(imageArray, i, j):
    """
    for a particular pixel, it return RGB value
    :param imageArray:
    :param i:
    :param j:
    :return:
    """
    R, G, B = imageArray
    return R[i][j], G[i][j], B[i][j]


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
    :return:
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


imageArray = load_image("RGB_Edition_7.jpg")
height = len(imageArray[0])  # getting image height
width = len(imageArray[0][0])  # getting  image width

inputvector = [127, 122]  # [127,130] will print bigger
print "Input vector is defined at : ", inputvector
BMUi, BMUj = findBMU(inputvector[0], inputvector[1], list(imageArray))
print "Best matching unit for input vector : ", inputvector, " , found at : ", BMUi, BMUj

# Lets plot for understanding
im = [[0 for x in range(height)] for y in range(width)]  # making 2d array
im[inputvector[0]][inputvector[1]] = 1  # plotting position of input vector in it
im[BMUi][BMUj] = 1  # plotting BMU in plot
plt.imshow(im, cmap='hot', interpolation='nearest')
plt.show()

# distance between two point 1) input vector and 2) BMU is considered as radius
Radius = findEucledeanDistanceBetweeenLattice(inputvector, [BMUi, BMUj])
print "Radius was found to be  : ", Radius
neighbours = findNeighbours([BMUi, BMUj], Radius, imageArray)
print "So Found Neighbours : ", neighbours
makeDummyImage(neighbours, imageArray)  # will make dummy image with circle around BMU considering radius
