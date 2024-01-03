import matplotlib.pyplot as plt
import pandas as pd
import numpy as np  

def kernel(point, xmat, k):
    m,n = np.shape(xmat)
    weights = np.mat(np.eye((m)))
    for j in range(m):
        diff = point - X[j]
        numerator = diff * diff.T
        denominator = 2.0 * k**2
        weights[j,j] = np.exp(numerator/(-denominator))
    return weights

def localWeight(point, xmat, ymat, k):
    weight = kernel(point, xmat, k)
    W = (X.T * (weight*xmat)).I * (X.T*(weight*ymat.T))
    return W

def localWeightRegression(xmat, ymat, k):
    rows,cols = np.shape(xmat)
    ypred = np.zeros(rows)
    for i in range(rows):
        ypred[i] = xmat[i]*localWeight(xmat[i], xmat, ymat, k)
    return ypred

def graphPlot(X, ypred):
    # Sort indices
    sortindex=X[:,1].argsort(0)
    xsort=X[sortindex][:,0]
    fig = plt.figure()
    subplotfig = fig.add_subplot(1,1,1)
    subplotfig.scatter(bill,tip,color='green')
    subplotfig.plot(xsort[:,1],ypred[sortindex],color='red',linewidth=5)
    # Setup labels
    plt.title('Locally Weighted Regression')
    plt.xlabel('Total Bill')
    plt.ylabel('Tip')
    # Show plot
    plt.show()

data = pd.read_csv('tips.csv')
bill = np.array(data.total_bill)
tip = np.array(data.tip)

mbill=np.mat(bill)
mtip=np.mat(tip)

m=np.shape(mbill)
one=np.mat(np.ones(m))
X=np.hstack((one.T,mbill.T))
ypred=localWeightRegression(X,mtip,1.5)
graphPlot(X, ypred)
