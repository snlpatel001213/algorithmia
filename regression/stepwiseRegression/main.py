"""
This python file was made to demonstarte use of all functions made in various class
in dataUtils and logitImplementation using dataset pima-indians-diabetes.data
obtained from  https://archive.ics.uci.edu/ml/machine-learning-databases/housing/housing.names
    1. CRIM      per capita crime rate by town
    2. ZN        proportion of residential land zoned for lots over
                 25,000 sq.ft.
    3. INDUS     proportion of non-retail business acres per town
    4. CHAS      Charles River dummy variable (= 1 if tract bounds
                 river; 0 otherwise)
    5. NOX       nitric oxides concentration (parts per 10 million)
    6. RM        average number of rooms per dwelling
    7. AGE       proportion of owner-occupied units built prior to 1940
    8. DIS       weighted distances to five Boston employment centres
    9. RAD       index of accessibility to radial highways
    10. TAX      full-value property-tax rate per $10,000
    11. PTRATIO  pupil-teacher ratio by town
    12. B        1000(Bk - 0.63)^2 where Bk is the proportion of blacks
                 by town
    13. LSTAT    % lower status of the population
    14. MEDV     Median value of owner-occupied homes in $1000's
"""

# importing all functionality
from stepWiseRegression import stepWiseRegressionModule

import dataUtils

# creating Instances
loadDataInstance = dataUtils.loadData()
minMaxNormalizationInstance = dataUtils.minMaxNormalization()
splitToTrainTestInstance = dataUtils.splitToTrainTest()
stepWiseRegressionInstance  = stepWiseRegressionModule()

# Running examples
crudedata = loadDataInstance.loadFromcsv('housing.data') #putting data from csv to array
floatData = loadDataInstance.convertDataToFloat(crudedata)  # converting string data to float one

minMax = minMaxNormalizationInstance.minMaxCalculator(floatData) # calculating min max for each column
normalizedData = minMaxNormalizationInstance.normalizeDatasetUsingMinmax(floatData,minMax)#appling min max normalization on entire dataset
X,Y = splitToTrainTestInstance.getXandY(normalizedData)
acceptedColsNo,coefficientValue =  stepWiseRegressionInstance.stepwise_Regression(X, Y, 0.01, 100,5) # training with logistic regression and stochastic gradient as a optimization function

print "Selected Columns : ", acceptedColsNo