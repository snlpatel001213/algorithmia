"""
LOOP BACK =1
1 HIDDEN LAYER OF 8 PERCEPTRON
"""

# IMPORTING ALL DEPENDENCIES
import numpy
import matplotlib.pyplot as plt
import pandas
from keras.models import Sequential
from keras.layers import Dense
CommonnOutputFile = open("accuracyComapre.csv","a+") # to write accuracy for al, currencies
# IMPORTING DATA IN PANDAS DATA FRAME
#ITRATING OVER ALL CURRENCIES
currencyArray = ["Date","USD","JPY","BGN","CYP","CZK","DKK","EEK","GBP","HUF","LTL","LVL","MTL","PLN","ROL","RON","SEK","SIT","SKK","CHF","ISK","NOK","HRK","RUB","TRL","TRY","AUD","BRL","CAD","CNY","HKD","IDR","INR","KRW","MXN","MYR","NZD","PHP","SGD","THB","ZAR","ILS"]
for currencyNo in range (1,len(currencyArray)):
    dataframe = pandas.read_csv('eurofxref-hist.csv', usecols=[currencyNo], engine='python')
    dataset = dataframe.values
    print dataset
    dataset = dataset.astype('float32')
    # LETS HAVE A LOOK AT THE DATA
    plt.suptitle("Exchange rate for "+currencyArray[currencyNo])
    plt.xlabel("No of Days")
    plt.ylabel("Exchange rate")
    plt.plot(dataset)
    # plt.show()
    plt.savefig("plots/"+currencyArray[currencyNo]+".png")
    plt.clf()
    # DEVIDING DATA SET IN TO TEST AND TRAIN
    train_size = int(len(dataset) * 0.67)  # 67% TRAIN
    test_size = len(dataset) - train_size  # REMIANING ~ 33% TEST
    train, test = dataset[0:train_size, :], dataset[train_size:len(dataset), :]
    # FUNCTION TO MAKE FEATURE AND PREDICATE IN TIME SERIES
    def create_dataset(dataset, look_back=1):
        dataX, dataY = [], []
        for i in range(len(dataset) - look_back - 1):
            a = dataset[i:(i + look_back), 0]
            dataX.append(a)
            dataY.append(dataset[i + look_back, 0])
        return numpy.array(dataX), numpy.array(dataY)


    # CREATING trainX, trainY testX AND testY USING create_dataset DATASET
    look_back = 1
    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)
    # DEFINING KERAS MODEL
    model = Sequential()
    model.add(Dense(8, input_dim=look_back, activation='relu'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, nb_epoch=200, batch_size=2, verbose=2)
    # MEASURING MODEL PERFORMANCE
    CommonnOutputFile.writelines(str(currencyArray[currencyNo])+",")
    print currencyArray[currencyNo]
    trainScore = model.evaluate(trainX, trainY, verbose=0)
    CommonnOutputFile.writelines(str(trainScore)+",")
    print trainScore,
    testScore = model.evaluate(testX, testY, verbose=0)
    CommonnOutputFile.writelines(str(testScore)+"\n")
    print testScore
    # GETTING PREDICTION ON TEST
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)
    print testPredict
    # PLOTTING
    trainPredictPlot = numpy.empty_like(dataset)
    trainPredictPlot[:, :] = numpy.nan
    trainPredictPlot[look_back:len(trainPredict) + look_back, :] = trainPredict
    # plt.plot(testPredict)
    # plt.show()
    # SHIFT TEST PREDICTION FOR PLOTTING
    testPredictPlot = numpy.empty_like(dataset)
    testPredictPlot[:, :] = numpy.nan
    testPredictPlot[len(trainPredict) + (look_back * 2) + 1:len(dataset) - 1, :] = testPredict
    # PLOT BASE LINE AND PREDICTIONS
    plt.suptitle("Predicted rate for " + currencyArray[currencyNo])
    plt.xlabel("No of Days")
    plt.ylabel("Exchange rate")
    plt.plot(dataset)
    plt.plot(trainPredictPlot)
    plt.plot(testPredictPlot)
    plt.savefig("plots/"+currencyArray[currencyNo] + "_result.png")
    plt.clf()
    CommonnOutputFile.flush()