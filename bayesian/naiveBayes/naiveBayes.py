import math

from utils import functionalTesting
from utils import loadData

# Dataset - https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)

loadDataInstance = loadData()
functionalTestingInstance = functionalTesting()

# load data
datasetInString = loadDataInstance.loadFromcsv("dataset/breast-cancer-wisconsin.data")
# convert to float
dataset = loadDataInstance.convertDataToFloat(datasetInString)


# making dictionary
def makeDictionaryFromDataset(dataset):
    """
    takes dataset as list of list
    :param dataset: [[5.0, 1.0, 1.0, 1.0, 2.0, 1.0, 3.0, 1.0, 1.0, 1.0],[5.0, 6.0, 5.0, 6.0, 10.0, 1.0, 3.0, 1.0, 1.0, 0.0],[4.0, 5.0, 1.0, 6.0, 2.0, 7.0, 3.0, 1.0, 1.0, 1.0]]
    :return:
    """
    classDict = {}
    for each in dataset:
        if each[-1] in classDict:
            # append the new number to the existing array at this slot
            classDict[each[-1]].append(
                each[:-1])  # each[-1] is a class , 0.0 or 1.0 | each[:-1] = all features except class
        else:
            # create a new array in this slot
            classDict[each[-1]] = [each[:-1]]
    return classDict  # {0.0:[[5.0, 6.0, 5.0, 6.0, 10.0, 1.0, 3.0, 1.0, 1.0]], 1.0:[[5.0, 1.0, 1.0, 1.0, 2.0, 1.0, 3.0, 1.0, 1.0],[4.0, 5.0, 1.0, 6.0, 2.0, 7.0, 3.0, 1.0, 1.0]]}


def getMean(array):
    """
    get array and return mean
    :param array:  [5.0, 6.0, 5.0, 6.0, 10.0, 1.0, 3.0, 1.0, 1.0]
    :return: float
    """
    return sum(array) / float(len(array))


def getStandardDeviation(array):
    """
    get array and return standard deviation
    :param array: [5.0, 6.0, 5.0, 6.0, 10.0, 1.0, 3.0, 1.0, 1.0]
    :return: float
    """
    average = getMean(array)
    variance = sum([math.pow(y - average, 2) for y in array]) / float(len(array) - 1)
    return variance


def gaussianProbabilityDensity(x, mean, stddev):
    """
    calculate gaussian Probability Density
    :param x: data; float
    :param mean:  data; float
    :param stddev:  data; float
    :return:
    """
    exponent = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stddev, 2))))
    return (1 / (math.sqrt(2 * math.pi) * stddev)) * exponent


# 70% of data, seperating for train
train = dataset[:int(len(dataset) * 0.7)]
print "Size of train dataset : ", len(train), " size of total dataset : ", len(dataset)
classDict = makeDictionaryFromDataset(train)

numberOfFeatures = len(dataset[0]) - 1  # number Of Features
# print numberOfFeatures # e.g. 0.9 Here
classes = classDict.keys()  # number of unique classes
# print  classes # e.g. [0.0, 1.0] Here

model = {}
for eachclass in classes:
    # print eachclass
    model[eachclass] = {}
    model[eachclass]['mean'] = []
    model[eachclass]['stddev'] = []
    for eachFeatureNo in range(numberOfFeatures):
        tempColumn = []
        for eachList in classDict[
            eachclass]:  # [[8.0, 2.0, 4.0, 1.0, 5.0, 1.0, 5.0, 4.0, 4.0],[5.0, 2.0, 3.0, 1.0, 6.0, 10.0, 5.0, 1.0, 1.0]]
            tempColumn.append(eachList[eachFeatureNo])  # tempColumn will be having any particular column
        # calculating mean for each feature
        model[eachclass]['mean'].append(getMean(tempColumn))
        # calculating stddev for each feature
        model[eachclass]['stddev'].append(getStandardDeviation(
            tempColumn))  # {0.0: {'stddev': [5.95045670637252, 7.381656962769089, 6.375327172693769, 10.368169435393417, 6.718337695635912, 9.712648896960653, 4.850595587842532, 10.829255915816487, 6.950296458522511], 'mean': [7.396907216494846, 6.298969072164948, 6.396907216494846, 5.304123711340206, 5.402061855670103, 7.675257731958763, 5.649484536082475, 5.84020618556701, 2.716494845360825]}, 1.0: {'stddev': [2.9417041392828223, 1.0992736077481833, 1.2235673930589215, 1.0448518390406987, 1.0773665398362717, 1.8841692609247165, 1.3593450939697855, 1.4419923901764191, 0.21692609247088446], 'mean': [2.833898305084746, 1.4067796610169492, 1.5084745762711864, 1.4067796610169492, 2.1864406779661016, 1.3864406779661016, 2.2813559322033896, 1.3864406779661016, 1.064406779661017]}}


def priorProbabilitycounter(className, dataset):
    """
    will calculate prior probability in given dataset for given class
    :param className:
    :param dataset:
    :return:
    usage: priorProbabilitycounter(1.0,train)
    """
    return float(len(classDict[className])) / float(len(dataset))


def likehoodCounter(x, featureNumber, className, dataset, classColumn):
    """
    will calculate likehood of given feature value to belong to particular class
    :param x: feature value
    :param featureNumber: feature number in as row
    :param className: class name for which likehood to be found
    :param dataset: dataset from which likehood reference to be taken
    :param classColumn: class column in the dataset
    :return:
    """
    likehoodCount = 0
    for eachRow in dataset:
        if (eachRow[featureNumber] == x and eachRow[classColumn] == className):
            likehoodCount = likehoodCount + 1
    getClassOccuranceCount = float(len(classDict[className]))
    return float(likehoodCount) / getClassOccuranceCount


print priorProbabilitycounter(1.0, train)
print likehoodCounter(5.0, 0, 1.0, train, 9)

# lets do testing
# Remaining 30% of data, separating for train
test = dataset[int(len(dataset) * 0.7):]
# print "Size of test data-set : ", len(test), " size of total data-set : ", len(dataset)


######################## predict for test ###########################
predictedClass = []
actualClass = []
for eachRow in test:  # iterating over each row
    classwiseProbability = [0] * len(
        classDict)  # classwiseProbability is an array which will store probability for both classes 0  and 1
    actualClass.append(int(eachRow[numberOfFeatures]))  # taking actual class for each row
    for eachclass in classes:  # for each class calculate likehood probability for each feature
        priorProb = priorProbabilitycounter(eachclass, train)  # calculate prior probability for class
        featureProbability = 1

        for eachfeatureNo in range(
                numberOfFeatures):  # calculating likehood probability for each feature and multiplying
            featureProbability = featureProbability * likehoodCounter(eachRow[eachfeatureNo], eachfeatureNo, eachclass,
                                                                      train, numberOfFeatures)
        overallProb = featureProbability * priorProb  # likehood probability multiplied with prior probability
        # print  eachclass, overallProb," |",
        classwiseProbability[
            int(eachclass)] = overallProb  # storing probability of perticular row to belong to either of class to array

    # converting probability to class, if probabilty for class 0 is higher then predictedClass = 0 else predictedClass = 1
    if classwiseProbability[0] > classwiseProbability[1]:  #
        predictedClass.append(0)
    else:
        predictedClass.append(1)

# getting performance matrix
functionalTestingInstance.createConfusionMatrix(actualClass, predictedClass, 0.95)
# False Positive :  5 , False Negative :  1 , True Positive :  158 , True Negative :  46 , Accuracy :  0.971428571429 , F1 Score :  0.981366459627
