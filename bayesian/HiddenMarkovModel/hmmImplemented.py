from collections import defaultdict
global  resultDict
resultDict = defaultdict(lambda : defaultdict(dict))


def resultDictgetter(observedStateNo,previousState,eachCurrentState):
    if observedStateNo ==2:
        previousState = 'initial'
        observedStateNo = observedStateNo - 1
        # print [observedStateNo],[previousState],[eachCurrentState]
        return resultDict[observedStateNo][previousState][eachCurrentState]
    else:
        observedStateNo = observedStateNo - 1
        return resultDict[observedStateNo][previousState][eachCurrentState]


def resultDictSetter(observedStateNo,previousState,currentState,value):
    resultDict[observedStateNo][previousState][currentState] = value

def givePath(resultDict,states):
    finalPath = []
    numberOfObservation = len (resultDict)
    for obsNo in  range(2,numberOfObservation+2):
        tempProb = []
        tempState = []
        for eachState in states:
            if obsNo == 2:
                previousState = 'initial'
                tempProb.append(resultDictgetter(obsNo,previousState,eachState))
                tempState.append(eachState)
                # print tempState, tempProb
            else:
                for eachCurrentState in states:
                    previousState = eachState
                    tempProb.append(resultDictgetter(obsNo, previousState, eachCurrentState))
                    tempState.append(eachCurrentState)
        if tempProb[0] > tempProb [1]:
            finalPath.append(tempState[0])
        else:
            finalPath.append(tempState[1])
        obsNo = obsNo + 1
        print finalPath




obs = ('normal', 'cold', 'dizzy')
states = ('Healthy', 'Fever')
start_p = {'Healthy': 0.6, 'Fever': 0.4}
trans_p = {
   'Healthy' : {'Healthy': 0.7, 'Fever': 0.3},
   'Fever' : {'Healthy': 0.4, 'Fever': 0.6}
   }
emit_p = {
   'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
   'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}
   }

# https://en.wikipedia.org/wiki/Viterbi_algorithm
observedStates = ['normal', 'cold', 'dizzy']


resultArray = []
observedStateNo  = 1
allStateProbability = {}
for eachObservedstate in observedStates:
    tempProb = {}
    for eachState in states:
        # print eachObservedstate
        if observedStateNo == 1: #for the first time entering in to calculation
            # taking initial probability in to consideration
            previousState = 'initial'
            # print eachObservedstate, eachState
            prob = start_p[eachState]*emit_p[eachState][eachObservedstate]
            resultDictSetter(observedStateNo, previousState,eachState, prob)
        else:
            for eachCurrentState in states:
                previousState = eachState
                if resultDictgetter(observedStateNo,eachCurrentState,previousState) < resultDictgetter(observedStateNo,eachCurrentState,eachCurrentState):
                    previousProb = resultDictgetter(observedStateNo,eachCurrentState,previousState)
                else:
                    previousProb =resultDictgetter(observedStateNo, eachCurrentState, eachCurrentState)
                print observedStateNo, previousState, eachCurrentState,previousProb , trans_p[eachState][eachCurrentState], emit_p[eachCurrentState][eachObservedstate]
                prob = previousProb * emit_p[eachState][eachObservedstate]*trans_p[eachState][eachCurrentState]
                resultDictSetter(observedStateNo, previousState, eachCurrentState, prob)
                print prob
                # tempStore[eachState] = prob
    observedStateNo = observedStateNo +1
givePath(resultDict,states)
