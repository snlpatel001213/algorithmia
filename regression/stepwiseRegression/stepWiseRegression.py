from math import exp

import dataUtils

loadDataInstance = dataUtils.loadData()


class stepWiseRegressionModule:
    def predict(self, Xrow, coefficients):
        """
        for prediction based on given row and coefficients
        :param Xrow:  [3.55565,4.65656,5.454654,1] where last element in a row remains Y [so called actual value y-actual]
        :param coefficients: [0.155,-0.2555,0.5456] Random initialization
        :return: Ypredicted

        This function will return coefficient as it is real thing we get after training
        coefficient  can be actually compared with memory from learning and be applied for further predictions

        """
        Ypredicted = coefficients[0]
        for i in range(len(Xrow)):
            Ypredicted += Xrow[i] * coefficients[i + 1]
        return 1.0 / (1.0 + exp(-Ypredicted))

    def decideGooodPredictors(self, Xtrain, Ytrain, learningRate, numberOfEpoches):
        """

        :param Xtrain:
        :param Ytrain:
        :param learningRate:
        :param numberOfEpoches:
        :return:
        """
        coefficient = [0.1 for i in range(len(Xtrain[0]) + 1)]
        # print coefficient

        for epoch in range(numberOfEpoches):
            """
            for each epoch repeat this operations
            """
            squaredError = 0
            averageError = 0.0
            for rowNo in range(len(Xtrain)):
                """
                for each row calculate following things
                where each row will be like this [3.55565,4.65656,5.454654,1] ==> where last element in a row remains Y [so called actual value y-actual]
                """
                # print Xtrain[rowNo]
                Ypredicted = self.predict(Xtrain[rowNo], coefficient)  # sending row and coefficient for prediction
                """
                row[-1] is last elemment of row, can be considered as Yactual; Yactual - Ypredicted gives error
                """
                error = Ytrain[rowNo] - Ypredicted
                "Updating squared error for each iteration"
                squaredError += error ** 2
                averageError = (averageError + squaredError) / 2
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
                coefficient[0] = coefficient[0] + learningRate * error * Ypredicted * (1 + Ypredicted)
                for i in range(len(Xtrain[rowNo])):
                    coefficient[i + 1] = coefficient[i + 1] + learningRate * error * Ypredicted * (1.0 - Ypredicted) * \
                                                              Xtrain[rowNo][i]
                    """
                    lets print everything as to know whether or not the error is really decreasing or not
                    """
            # print (">>> Epoch : ", epoch, " | Error : ", squaredError, "| Average Error : ", averageError)
        return averageError,coefficient
    def accepetedColumns(self,RsquareValue,maxPredictor):
        """
        get column with least r square value
        :param RsquareValue: An array with R square value
        e.g. [12.399790911951232, 11.14467573048574, 10.99939946366844, 12.313118044897763, 11.812905343161896, 8.530664160073936, 11.642709319002446, 12.377547637064676, 12.376152652375172, 11.935468510009718, 10.221164713630898, 12.258299424118913, 8.627925610329616]
        :param maxPredictor: An integer indicating number of column out of these to be selected e.g. 4
        :return: selected column number [5, 11, 9, 2] A list
        """
        acceptedColsNo = []
        for i in range(maxPredictor):
            minValue = min(RsquareValue)
            acceptedColsNo.append(RsquareValue.index(minValue))
            RsquareValue.remove(minValue)
        return acceptedColsNo


    def stepwise_Regression(self, Xtrain, Ytrain, learningRate, numberOfEpoches, maxPredictor):
        """

        :param Xtrain: 2D array
        :param Ytrain: 2d Array
        :param learningRate: float between 0 and 1
        :param numberOfEpoches: any integer
        :param maxPredictor: number of column to be selected for final run with highest correlation with predicate
        :return: Its prints , return Rsquarerror and coefficient value for selected column
        e.g.
        (7.5460202999842885, [-0.04315767605226367, 1.165157142272148, -0.45268840110500463, -0.43397502762968604, -0.7226568412142056])
        """
        """
        For each column in train dataset we will be having one coefficient
        if training dataset having 5 column per array than
        coefficient array will be something like this [0.0, 0.0, 0.0, 0.0, 0.0]
        """
        RsquareValue = []
        for columnNo in range(0, len(Xtrain[0])):
            "getting Rsquare error for each column"
            XColumn = loadDataInstance.getSpecificColumns(Xtrain, [columnNo])
            RsquareValue.append(self.decideGooodPredictors(XColumn, Ytrain, learningRate, numberOfEpoches)[0])
        print RsquareValue
        "getting maxcolumn e.g. maxPredictor with lowerst error"
        acceptedColsNo = self.accepetedColumns(RsquareValue, maxPredictor)
        "Making prediction on selected column"
        XColumn = loadDataInstance.getSpecificColumns(Xtrain, acceptedColsNo)
        print acceptedColsNo
        return self.decideGooodPredictors(XColumn, Ytrain, learningRate, numberOfEpoches)

