from collections import defaultdict

global resultDict
resultDict = defaultdict(lambda: defaultdict(dict))

# https://en.wikipedia.org/wiki/Viterbi_algorithm

obs = ('normal', 'cold', 'dizzy')
states = ('Healthy', 'Fever')
start_p = {'Healthy': 0.6, 'Fever': 0.4}
trans_p = {
    'Healthy': {'Healthy': 0.7, 'Fever': 0.3},
    'Fever': {'Healthy': 0.4, 'Fever': 0.6}
}
emit_p = {
    'Healthy': {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
    'Fever': {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}
}

observation = ['normal', 'cold', 'dizzy']


def initializeDict(observationLength, states):
    """
    initializeDict(len(observedStates),states)
    :param observedStatesLength:
    :param states:
    :return:     defaultdict(<function <lambda> at 0x7f280b5f0cf8>, {1: defaultdict(<type 'dict'>, {'Healthy': 0, 'Fever': 0}), 2: defaultdict(<type 'dict'>, {'Healthy': 0, 'Fever': 0}), 3: defaultdict(<type 'dict'>, {'Healthy': 0, 'Fever': 0})})
    """
    for i in range(observationLength):
        for eachState in states:
            resultDict[i][eachState] = 0



def dictSetter(eachState, observationNo, prob):
    """
    set values to dictionary
    :param eachState:
    :param observationNo:
    :param prob:
    :return:
    """
    if float(prob) > float(resultDict[observationNo][eachState]):
        resultDict[observationNo][eachState] = prob


def dictGetter(eachState, observationNo):
    """
    getting values from dictionary
    :param eachState:
    :param observationNo:
    :return:
    """
    return resultDict[observationNo][eachState]


def getHiddenPath(resultDict):
    """
    to get hidden path, which was responsible for observed sequence
    :param resultDict:
    :return:
    """
    path = []
    for eachObservationNo in range(len(resultDict)):
        prob = []
        for eachstate in states:
            prob.append(resultDict[eachObservationNo][eachstate])
        path.append(states[prob.index(max(prob))])
    return path



# main function to perform everything
initializeDict(len(observation), states)
for observationNo in range(len(observation)): # iterating through all observation
    # print observed[observedNo]
    for eachState in states: # iterating through each state
        # for first observedstate
        if observationNo == 0: # for first observation # take initil probabilities in to consideration
            prob = start_p[eachState] * emit_p[eachState][observation[observationNo]]
            # print prob
            dictSetter(eachState, observationNo, prob)
        else:
            for eachCurrentState in states:  # for subsequent observation
                # print "previous  : ",eachState," | Current State : ",eachCurrentState, " | observationNo : ",observationNo
                previousProb = dictGetter(eachState, observationNo - 1)
                # print previousProb, trans_p[eachState][eachCurrentState], emit_p[eachCurrentState][observation[observationNo]],
                prob = trans_p[eachState][eachCurrentState] * emit_p[eachCurrentState][[observationNo]] * previousProb
                # print prob
                dictSetter(eachCurrentState, observationNo, prob) # set to dictionary

print getHiddenPath(resultDict)
