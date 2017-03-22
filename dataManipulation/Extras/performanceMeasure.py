"""
Written by sunil Patel
snlpatel001213[-@-]hotmail.com
"""

def createConfusionMatrix(self, actual, predicted, threshold):
    """
    will create confusion matrix for given set of actual and predicted array
    Sometime insted of 1 and 0, we have probabilistic value [any float between 1 and 0], so threshold is required
    :param actual: Array of Actual sample
    :param predicted: Array of predicted sample
    :param threshold:  Any number between 0-1
    :return:
    """
    fp = 0
    fn = 0
    tp = 0
    tn = 0
    for i in range(len(predicted)):
        # if  predicted value is greater than threshold, predicted value = 1 else predicted value = 0
        if predicted[i] > threshold:
            predicted[i] = 1
        else:
            predicted[i] = 0
    for no in range(0, len(predicted)):
        if predicted[no] == 1 and actual[no] == 1:
            tp += 1
        elif predicted[no] == 0 and actual[no] == 0:
            tn += 1
        elif predicted[no] == 1 and actual[no] == 0:
            fn += 1
        elif predicted[no] == 0 and actual[no] == 1:
            fp += 1
    # calculating accuracy
    ACC = float((tp + tn)) / float((fp + tp + tn + fn))
    # calculating f1 measure
    F1 = float(2 * tp) / float(2 * tp + fp + fn)
    print "False Positive : ", fp, ", False Negative : ", fn, ", True Positive : ", tp, ", " \
                                                                                        "True Negative : ", tn, ", Accuracy : ", ACC, ", F1 Score : ", F1