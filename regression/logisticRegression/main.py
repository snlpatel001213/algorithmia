"""
This python file was made to demonstarte use of all functions made in various class
in dataUtils and logitImplementation using dataset pima-indians-diabetes.data
obtained from  https://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data
"""
# importing all functionality
import dataUtils
from  logitImplementation import logisticRegression

# creating Instances
loadDataInstance = dataUtils.loadData()
minMaxNormalizationInstance = dataUtils.minMaxNormalization()
splitToTrainTestInstance = dataUtils.splitToTrainTest()
logisticRegressionInstance  = logisticRegression()
functionalTestingInstance =  dataUtils.functionalTesting()


# Running examples
crudedata = loadDataInstance.loadFromcsv('pima-indians-diabetes.data') #putting data from csv to array
floatData = loadDataInstance.convertDataToFloat(crudedata)  # converting string data to float one
minMax = minMaxNormalizationInstance.minMaxCalculator(floatData) # calculating min max for each column
normalizedData = minMaxNormalizationInstance.normalizeDatasetUsingMinmax(floatData,minMax) #appling min max normalization on entire dataset
train,test = splitToTrainTestInstance.basicSplitter(normalizedData) #splitting in to train and test data
coefficient =  logisticRegressionInstance.stochastic_gradient(train,0.3,500) # training with logistic regression and stochastic gradient as a optimization function
actual,predicted =logisticRegressionInstance.predictOnTest(test,coefficient) # =testing on remining 30% of data
functionalTestingInstance.createConfusionMatrix(actual,predicted,0.30) # getting confusion matrix, accuracy and F1 score

