import csv

import numpy as np
from matplotlib import pyplot as plt
from sklearn.manifold import TSNE


def loadDataset(filename, numattrs):
    """
    loads data from file
    :param filename:
    :param numattrs: number of column in file, Excluding  class column
    :return:
    """
    csvfile = open(filename, 'r')
    lines = csv.reader(csvfile)
    dataset = list(lines)
    for x in range(len(dataset)):
        for y in range(numattrs):
            dataset[x][y] = float(dataset[x][y])
    return dataset


# loading data from iris.csv
XY = loadDataset("iris.csv", numattrs=4)
X = np.asarray(XY)[:, :4]  # skipping class column
Y = np.asarray(XY)[:, 4:]  # taking only class column

# converting to numerical values
Y = reduce(lambda x, y: x + y, Y.tolist())  # flattening class values [[X],[Y],[X]] == > [X,Y,X]
Uniquelabels = list(set(
    Y))  # Finding Number of unique labels  [X,Y] will be having something this Set('Iris-setosa','Iris-versicolor','Iris-virginica')

# converting categorical class value to numerical one
YNumeric = []
for each in Y:
    """
    This loop will convert categorical classes ('Iris-setosa','Iris-versicolor','Iris-virginica') to numerical one e.g. 1,2,3 respectively
    """
    YNumeric.append(Uniquelabels.index(each))

# print YNumeric

# plotting after applying t-nse
X_tsne = TSNE(learning_rate=100).fit_transform(X)
plt.figure(figsize=(10, 5))
plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=YNumeric)

plt.show()
