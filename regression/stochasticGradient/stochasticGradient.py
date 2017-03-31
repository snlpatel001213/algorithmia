def predict(Xrow, coefficients):
    """
    for prediction based on given row and coefficients
    :param Xrow:  [1,0,0] where last element in a row remains Y [so called actual value y-actual]
    :param coefficients: [0.155,-0.2555,0.5456] Random initialization
    :return: Ypredicted

    This function will return coefficient as it is real thing we get after training
    coefficient  can be actually compared with memory from learning and be applied for further predictions
    """
    """
    Ypredicted = b0 + BaXa + BbXb

    Ypredicted = coefficients[0] - will take bo in to Ypredicted

    Ypredicted += Xrow[i] * coefficients[i + 1] - Ba and Bb are multiplies to Xa and Xb gives BaXa + BbXb
    """
    Ypredicted = coefficients[0]
    for i in range(len(Xrow) - 1):
        Ypredicted += Xrow[i] * coefficients[i + 1]
    return Ypredicted # Ypredicted is return back


def SGD(dataset, learningRate, numberOfEpoches):
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
    coefficient = [0.1 for i in range(len(dataset[0]))]
    for epoch in range(numberOfEpoches):
        """
        for each epoch repeat this operations
        """
        squaredError = 0
        for row in dataset:
            """
            for each row calculate following things
            where each row will be like this [3.55565,4.65656,5.454654,1] ==> where last element in a row remains Y [so called actual value y-actual]
            """
            Ypredicted = predict(row, coefficient)  # sending row and coefficient for prediction
            error = row[
                        -1] - Ypredicted  # row[-1] is last elemment of row, can be considered as Yactual; Yactual - Ypredicted gives error
            "Updating squared error for each iteration"
            squaredError += error ** 2
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
            for i in range(len(row) - 1):
                coefficient[i + 1] = coefficient[i + 1] + learningRate * error * Ypredicted * (1.0 - Ypredicted) * row[
                    i]

                """
                lets print everything as to know whether or not the error is really decreasing or not
                """
        print "Epoch : ", epoch, " , squared Error : ", squaredError
    return coefficient


data = [[1, 1, 1], [0, 1, 0], [1, 0, 0], [0, 0, 0]]
# run SGD
SGD(data, .1, 250)
