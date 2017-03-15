"""
This python file was made to demonstarte use of all functions made in various class
in dataUtils and logitImplementation using dataset pima-indians-diabetes.data
obtained from  https://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data
"""
# importing all functionality
from  stepwiseRegression import stepWiseRegression

import dataUtils

# creating Instances
loadDataInstance = dataUtils.loadData()
minMaxNormalizationInstance = dataUtils.minMaxNormalization()
splitToTrainTestInstance = dataUtils.splitToTrainTest()
stepWiseRegressionInstance  = stepWiseRegression.stepWiseRegressionModule()
functionalTestingInstance =  dataUtils.functionalTesting()


# Running examples
crudedata = loadDataInstance.loadFromcsv('housing.data') #putting data from csv to array
floatData = loadDataInstance.convertDataToFloat(crudedata)  # converting string data to float one
minMax = minMaxNormalizationInstance.minMaxCalculator(floatData) # calculating min max for each column
normalizedData = minMaxNormalizationInstance.normalizeDatasetUsingMinmax(floatData,minMax)#appling min max normalization on entire dataset
X,Y = splitToTrainTestInstance.getXandY(normalizedData)
Xtrain, Xtest, Ytrain, Ytest = splitToTrainTestInstance.basicSplitter(X,Y) #splitting in to train and test data
# print Ytrain
coefficient =  stepWiseRegressionInstance.stepwise_Regression(Xtrain, Ytrain, 0.01, 100,4) # training with logistic regression and stochastic gradient as a optimization function
# actual,predicted =stepWiseRegression.predictOnTest(test,coefficient) # =testing on remining 30% of data
# functionalTestingInstance.createConfusionMatrix(actual,predicted,0.30) # getting confusion matrix, accuracy and F1 score