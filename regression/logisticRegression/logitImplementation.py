from math import exp


class logisticRegression:
    def predict(self, Xrow,coefficients):
        """
        for prediction based on given row and coefficients
        :param Xrow:  [3.55565,4.65656,5.454654,1] where last element in a row remains Y [so called actual value y-actual]
        :param coefficients: [0.155,-0.2555,0.5456] Random initialization
        :return: Ypredicted

        This function will return coefficient as it is real thing we get after training
        coefficient  can be actually compared with memory from learning and be applied for further predictions

        """
        Ypredicted = coefficients[0]
        for i in range(len(Xrow)-1):
            Ypredicted += Xrow[i]*coefficients[i+1]
        return 1.0/(1.0+exp(-Ypredicted))

    def stochastic_gradient(self, trainDataset, learningRate, numberOfEpoches):
        """
        :param trainDataset:
        :param learningRate:
        :param numberOfEpoches:
        :return: updated coefficient array
        """
        """
        For each column in train dataset we will be having one coefficient
        if training dataset having 5 column per array than
        coefficient array will be something like this [0.0, 0.0, 0.0, 0.0, 0.0]
        """
        coefficient = [0.1 for i in range(len(trainDataset[0]))]
        for epoch in range(numberOfEpoches):
            """
            for each epoch repeat this operations
            """
            squaredError = 0
            for row in trainDataset:
                """
                for each row calculate following things
                where each row will be like this [3.55565,4.65656,5.454654,1] ==> where last element in a row remains Y [so called actual value y-actual]
                """
                Ypredicted = self.predict(row,coefficient) # sending row and coefficient for prediction
                error = row[-1] - Ypredicted #row[-1] is last elemment of row, can be considered as Yactual; Yactual - Ypredicted gives error
                "Updating squared error for each iteration"
                squaredError += error**2
                """
                In order to make learning, we should learn from our error
                here  we will use stochastic gradient as a optimization function
                Stochastic gradient for each coefficient [b0,b1,b1,.....] can be formalized as
                coef[i+1]  =  coef[i+1] + learningRate * error * Ypredicted(1.0 - Ypredicted)* X[i]

                For a row containing elements [x1, x2, x3, x4, x5], coefficient  [bo, b1, b2, b3, b4, b5]
                  where each coefficient belongs to each element in a row
                  e.g. b1 for X1, b2 for x2 and so on..
                As coefficient[i] here is equal to bo, e.g. row element independent, we will update it separately.
                """
                coefficient[0] = coefficient[0]+learningRate*error*Ypredicted*(1+Ypredicted)
                for i in range (len(row)-1):
                    coefficient[i+1] = coefficient[i+1] + learningRate * error * Ypredicted*(1.0 - Ypredicted)* row[i]

                    """
                    lets print everything as to know whether or not the error is really decreasing or not
                    """
            print (">>> Epoch : ", epoch," | Error : " ,squaredError)

        return coefficient

    def predictOnTest(self,testDataset, coefficient):
        """
        predicting on leftover dataset
        :param testDataset: test dataset Array of array
        :param coefficient: Array of coefficient
        :return: actualvalues [Array],predictedlist [Array]
        """
        file = open("logs", "w")
        actual  = []
        predictedlist = []
        for row in testDataset:
            actual.append(row[-1])
            predicted = coefficient[0]
            for i in range(len(row)-1):
                predicted +=row[i]*coefficient[i+1]
            predicted = 1.0/(1.0+exp(-predicted))
            predictedlist.append(predicted)
            file.write(str(predicted)+"\t"+str(row[-1])+"\n")
            print ("predicted : ",predicted, " | Actual : ",row[-1] )
        return actual,predictedlist
