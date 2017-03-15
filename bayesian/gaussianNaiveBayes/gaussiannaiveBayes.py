from utils import loadData
from utils import splitToTrainTest
from utils import functionalTesting
import math
# Dataset - https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)

loadDataInstance  = loadData()
functionalTestingInstance =  functionalTesting()

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
            classDict[each[-1]].append(each[:-1]) # each[-1] is a class , 0.0 or 1.0 | each[:-1] = all features except class
        else:
            # create a new array in this slot
            classDict[each[-1]] =[each[:-1]]
    return classDict  #{0.0:[[5.0, 6.0, 5.0, 6.0, 10.0, 1.0, 3.0, 1.0, 1.0]], 1.0:[[5.0, 1.0, 1.0, 1.0, 2.0, 1.0, 3.0, 1.0, 1.0],[4.0, 5.0, 1.0, 6.0, 2.0, 7.0, 3.0, 1.0, 1.0]]}

def getMean(array):
    """
    get array and return mean
    :param array:  [5.0, 6.0, 5.0, 6.0, 10.0, 1.0, 3.0, 1.0, 1.0]
    :return: float
    """
    return sum(array)/float(len(array))

def getStandardDeviation(array):
    """
    get array and return standard deviation
    :param array: [5.0, 6.0, 5.0, 6.0, 10.0, 1.0, 3.0, 1.0, 1.0]
    :return: float
    """
    average =  getMean(array)
    variance = sum([math.pow(y-average,2) for y in array])/float(len(array)-1)
    return variance
def gaussianProbabilityDensity(x,mean,stddev):
    """
    calculate gaussian Probability Density
    :param x: data; float
    :param mean:  data; float
    :param stddev:  data; float
    :return:
    """
    exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stddev,2))))
    return (1/(math.sqrt(2*math.pi)*stddev))*exponent




# 70% of data, seperating for train
train = dataset[:int(len(dataset)*0.7)]
print "Size of train dataset : ", len(train), " size of total dataset : ", len(dataset)
classDict = makeDictionaryFromDataset(train)



numberOfFeatures = len(dataset[0])-1 # number Of Features
# print numberOfFeatures # e.g. 0.9 Here
classes = classDict.keys() # number of unique classes
# print  classes # e.g. [0.0, 1.0] Here

model = {}
for eachclass in classes:
    # print eachclass
    model[eachclass] = {}
    model[eachclass]['mean'] = []
    model[eachclass]['stddev'] = []
    for eachFeatureNo in range(numberOfFeatures):
        tempColumn = []
        for eachList in classDict[eachclass]: #[[8.0, 2.0, 4.0, 1.0, 5.0, 1.0, 5.0, 4.0, 4.0],[5.0, 2.0, 3.0, 1.0, 6.0, 10.0, 5.0, 1.0, 1.0]]
            tempColumn.append(eachList[eachFeatureNo]) # tempColumn will be having any particular column
        # calculating mean for each feature
        model[eachclass]['mean'].append(getMean(tempColumn))
        # calculating stddev for each feature
        model[eachclass]['stddev'].append(getStandardDeviation(tempColumn)) #{0.0: {'stddev': [5.95045670637252, 7.381656962769089, 6.375327172693769, 10.368169435393417, 6.718337695635912, 9.712648896960653, 4.850595587842532, 10.829255915816487, 6.950296458522511], 'mean': [7.396907216494846, 6.298969072164948, 6.396907216494846, 5.304123711340206, 5.402061855670103, 7.675257731958763, 5.649484536082475, 5.84020618556701, 2.716494845360825]}, 1.0: {'stddev': [2.9417041392828223, 1.0992736077481833, 1.2235673930589215, 1.0448518390406987, 1.0773665398362717, 1.8841692609247165, 1.3593450939697855, 1.4419923901764191, 0.21692609247088446], 'mean': [2.833898305084746, 1.4067796610169492, 1.5084745762711864, 1.4067796610169492, 2.1864406779661016, 1.3864406779661016, 2.2813559322033896, 1.3864406779661016, 1.064406779661017]}}


#WHAT EVER IS THERE IN model IS CALLED NAIVE BAISE MODEL HERE
# IT LOOKS LIKE THIS
print "MODEL : ",model
# BASED ON model, WE WILL CALCULATE GAUSSIAN PROBABILITY DENSITY THAT WILL SERVE AS ULTIMATE CLASSIFIER.

# lets do testing
# Remaining 30% of data, separating for train
test = dataset[int(len(dataset)*0.7):]
print "Size of test data-set : ", len(test), " size of total data-set : ", len(dataset)

def predict(features,model):
    """
    Will do prediction on test data based on model so generated.
    :param features: [8.0, 2.0, 4.0, 1.0, 5.0, 1.0, 5.0, 4.0, 4.0] only features, no class
    :param model: can be considered as model
    :return:
    """
    combinedProbability = {} # a dictionary where probability for each feature of each class will be saved
    for eachclass in classes:
        combinedProbability[eachclass] = []
    for eachFeatureNo in range(numberOfFeatures):
        for eachclass in classes:
            meanForFeature = model[eachclass]['mean'][eachFeatureNo] # get mean for that particular feature of class from model
            stddevForFeature = model[eachclass]['stddev'][eachFeatureNo] # get stddev for that particular feature of class from model
            gpd = gaussianProbabilityDensity(features[eachFeatureNo],meanForFeature,stddevForFeature) #calculate gaussian Probability Density for that feature for both class
            combinedProbability[eachclass].append(gpd)  # store gaussian predicted probability for each class for each feature
                                                        #{0.0: [6.651930570966195e-17, 9.154229062240036e-131, 1.4689405384278686e-172, 0.0, 1.6667067014825224e-58, 8.24203399075415e-279, 1.0334229828147304e-15, 0.0, 7.123285287614845e-33], 1.0: [1.9757527520696125e-20, 0.07829567060266986, 0.27210727230597875, 0.3488418781229466, 0.25218666596082123, 1.1483036351939655e-06, 0.019160052488986935, 0.23687445105815633, 1.838890565762708]}
    # print combinedProbability

    # class probability is equal to multiplication of each individual feature probabilities
    classprobability = [0] * len(classes)
    for eachClass in combinedProbability.keys():
        allFeatureProbability = 1
        for eachProbability in combinedProbability[eachClass]:
            allFeatureProbability = allFeatureProbability * eachProbability
            # allFeatureProbability  multiplying all feature probabilities
        classprobability[int(eachClass)] = allFeatureProbability
    return classprobability # store probability for each class [1.445545,-0.456825] , for class 0 and 1 respectively

originalClass = [] # will store original class
predictedClass= [] # will store predicted class

for eachtestsample in test: #iter through test
    originalClass.append(int(eachtestsample[-1]))  # getting original class for each test sample
    onlyFeatures = eachtestsample[:-1] # getting features for each test sample
    predicteProbability = predict(onlyFeatures,model)   # predicted probability per class

    # converting probability to class, if probabilty for class 0 is higher then predictedClass = 0 else predictedClass = 1
    if predicteProbability[0] > predicteProbability[1]:
        predictedClass.append(0)
    else:
        predictedClass.append(1)
# you may print this to see original and predicted classes value
# print originalClasses
# print predictedCalsses

# getting accuracy measures
functionalTestingInstance.createConfusionMatrix(originalClass, predictedClass, 0.95)
# False Positive :  3 , False Negative :  1 , True Positive :  160 , True Negative :  46 , Accuracy :  0.980952380952 , F1 Score :  0.987654320988
