import pandas as pd
import math
import numpy as np

data = pd.read_csv("./playtennis.csv")
features = [feature for feature in data]
features.remove("Answer")

class Node:
    def __init__(self):
        self.children = []
        self.value = ""
        self.isLeaf = False
        self.pred = ""

def entropy(exampleset):
    pos = 0.0
    neg = 0.0
    for _, row in exampleset.iterrows():
        if row["Answer"] == "yes":
            pos += 1
        else:
            neg += 1
    
    if pos == 0.0 or neg == 0.0:
        return 0.0
    else:
        p = pos / (pos+neg)
        n = neg / (pos+neg)
        return -( p*math.log(p,2) + n*math.log(n,2) )

def info_gain(dataset, attr):
    unique_values = np.unique(dataset[attr]) # list of unique values for that attribute
    gain = entropy(dataset) # find entropy of entire dataset passed

    for value in unique_values:
        subdata = exampleset[exampleset[attr] == u]
        sub_e = find_entropy(subdata)
        gain -= (float(len(subdata)))/(float(len(exampleset))) * sub_e
    
    return gain