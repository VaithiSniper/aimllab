from numpy import positive
import pandas as pd

# globals
total_instances = 0
total_positive_instances = 0
total_negative_instances = 0

def readDataSet():
    global total_instances, total_positive_instances, total_negative_instances
    # read csv file
    data = pd.read_csv('data.csv')
    # get total instances
    total_instances = len(data)
    total_positive_instances = len(data.loc[data[data.columns[-1]] == 'Yes'])
    total_negative_instances = total_instances - total_positive_instances
    # get training set
    trainingSet = data.sample(frac=0.75,replace=False)
    # get test set
    testSet = pd.concat([data, trainingSet]).drop_duplicates(keep=False)
    # print("Training Set\n", trainingSet)
    # print("\nTest Set\n", testSet)
    return trainingSet, testSet, data

def calculateProbability(trainingSet, testSet, data):
    probabilityMap = {}
    # calculate probability of each attribute
    for col in trainingSet.columns[:-1]:
        probabilityMap[col] = {}
        possibleValues = set(data[col])
        for value in possibleValues:
            rowsWithAttributeValue = (trainingSet.loc[trainingSet[col]==value])
            positiveInstances = rowsWithAttributeValue.loc[rowsWithAttributeValue[rowsWithAttributeValue.columns[-1]] == 'Yes']
            negativeInstances = rowsWithAttributeValue.loc[rowsWithAttributeValue[rowsWithAttributeValue.columns[-1]] == 'No']
            probabilityMap[col][value] = [len(positiveInstances)/len(rowsWithAttributeValue), len(negativeInstances)/len(rowsWithAttributeValue)]
    return probabilityMap

def testInstanceForPrediction(testInstance, probabilityMap, expectedValue, columnHeaders):
    cumulativePositiveProbability = total_positive_instances/total_instances
    cumulativeNegativeProbability = total_negative_instances/total_instances
    for col in columnHeaders:
        pickedProbPositive = probabilityMap[col][testInstance[col]][0]
        pickedProbNegative = probabilityMap[col][testInstance[col]][1]
        cumulativePositiveProbability *= pickedProbPositive
        cumulativeNegativeProbability *= pickedProbNegative
    prediction = 'Yes' if cumulativePositiveProbability > cumulativeNegativeProbability else 'No'
    return True if prediction == expectedValue else False

def calculateAccuracy(probabilityMap, testSet):
    correctPredictions = 0
    for i in range(len(testSet)):
        testInstance = testSet.iloc[i,:]
        if testInstanceForPrediction(testInstance, probabilityMap, testInstance[-1], testSet.columns[:-1]):
            correctPredictions += 1
    return correctPredictions/len(testSet)

def main():
    trainingSet, testSet, data = readDataSet()
    probabilityMap = calculateProbability(trainingSet, testSet, data)
    print("----------------------------------------")
    print("Probability Map\n", probabilityMap)
    print("----------------------------------------")
    accuracy = calculateAccuracy(probabilityMap, testSet)
    print("----------------------------------------")
    print("Accuracy: ", accuracy)


main()
