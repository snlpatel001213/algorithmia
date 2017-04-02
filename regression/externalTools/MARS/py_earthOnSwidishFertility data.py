import numpy
import matplotlib.pyplot as plt
from pyearth import Earth
import csv
import traceback

def loadFromcsv( fileName):
    """
    load a file and conver to 2d python list and return it
    :param fileName: csv file name with absolute path

    Example file  - pima-indians-diabetes.data
    Test the script using following code
    loadDataInstance =  loadData()
    print loadDataInstance.loadFromcsv('pima-indians-diabetes.data')
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


dataset = loadFromcsv("SwidishFertility.txt") # loading dataset
dataset =  convertDataToFloat(dataset) # converting string to float


xArray = []
yArray = []

#seperating X and Y from the dataset
for eachXYPAir in dataset:
    x = eachXYPAir[0]
    y = eachXYPAir[1]
    xArray.append(x)
    yArray.append(y)

# print len(xArray)
xArray =  numpy.asarray(xArray,"float32") # converting to numpy array
# print len(yArray)
yArray =  numpy.asarray(yArray,"float32") # converting to numpy array
# Fit an Earth model
model = Earth(max_degree=1, verbose=True) # initializing py- earth package

# making model for the data
model.fit(xArray, yArray)

# Print the model
print(model.trace())
print(model.summary())


# Plot the model
y_hat = model.predict(xArray)
# print y_hat
plt.figure()
plt.plot(xArray, yArray, 'r.')
plt.plot(xArray, y_hat, 'b.')
plt.show()