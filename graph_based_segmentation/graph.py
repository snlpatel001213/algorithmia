import math

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy import ndimage
import networkx as nx



def initilaize_graph(number):
    G = nx.Graph()
    G = nx.cycle_graph(number)
    return G

def load_image(infilename):
    """
    will load image from the file
    :param infilename: filename
    :return: numpy array of image
    """
    img = ndimage.imread(infilename)
    data = np.asarray(img, dtype="int32")
    image_height = data.shape[0]
    image_width = data.shape[1]
    return data,image_height,image_width


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
    """
    converting image to numpy array
    :param img:
    :return:
    """
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

def find_distance(lattice1, lattice2):
    """
    if two point on 2d surface are given, it will return distance between two points
    :param lattice1: list [x,y]
    :param lattice2: list [x1,y1]
    :return:
    """
    return math.sqrt(math.pow(lattice1[0] - lattice2[0], 2) + math.pow(lattice1[1] - lattice2[1], 2) + math.pow(lattice1[2] - lattice2[2], 2))

def get_lattice(pixel_number, image_height, image_width):
    """
    get x and  y location from given pixel number
    :param pixel_number:
    :param image_height:
    :param image_width:
    :return:
    """
    loc_row = int(pixel_number/ image_width)
    loc_col = pixel_number % image_width
    return [loc_row, loc_col]
