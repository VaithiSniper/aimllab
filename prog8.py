import csv
import math
import random
import operator

def loadDataset(file, split, trainingSet = [], testSet = []):
    with open(file, 'r') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for x in range(len(dataset)):
            for y in range(4):
                dataset[x][y] = float(dataset[x][y])
            if random.random() < split:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])

def distance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow(instance1[x] - instance2[x], 2)
    return math.sqrt(distance)
    
def getNeighbours(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        dist = distance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x],dist))
    distances.sort(key=operator.itemgetter(1))
    neighbours = []
    for x in range(k):
        neighbours.append(distances[x][0])
    return neighbours

def getResponse(neighbours):
    classVotes = {}
    for x in range(len(neighbours)):
        vote = neighbours[x][-1]
        existingVotes = classVotes.setdefault(vote, 0)
        classVotes[vote] += 1
    return sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)[0][0]

def getAccuracy(testSet, predictions):
    correctCount = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correctCount += 1
    return (correctCount/float(len(testSet)))*100.0

def main():
    trainingSet = []
    testSet = []
    split = 0.3
    loadDataset("KNN-input.csv",split, trainingSet, testSet)
    print ('\n Number of Training data: ' + (repr(len(trainingSet))))
    print (' Number of Test Data: ' + (repr(len(testSet))))
    # generate predictions
    print('\n The predictions are: ')
    predictions=[]
    k=3
    for i in range(len(testSet)):
        instance = testSet[i]
        neighbours = getNeighbours(trainingSet, instance, k)
        response = getResponse(neighbours)
        predictions.append(response)
        print('predicted = '+repr(response), 'actual value = '+repr(instance[-1]))
    accuracy = getAccuracy(testSet, predictions)
    print("Accuracy of model is :"+repr(accuracy)+"%")

main()