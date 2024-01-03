from sklearn import datasets
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture

iris = datasets.load_iris()

x = pd.DataFrame(iris.data)
x.columns = ['Sepal_Length','Sepal_Width','Petal_Length','Petal_Width']

y = pd.DataFrame(iris.target)
y.columns = ['Targets']

colormap = np.array(['red','lime','black'])

plt.subplot(1,2,1)
plt.scatter(x.Sepal_Length, x.Sepal_Width, c=colormap[y.Targets], s=40)
plt.title('Real Clustering')
plt.show()

model = KMeans(n_clusters=3)
model.fit(x)

plt.subplot(1,2,2)
plt.scatter(x.Sepal_Length, x.Sepal_Width, c=colormap[model.labels_], s=40)
plt.title('K Mean Classification')

model2 = GaussianMixture(n_components=3)
model2.fit(x)

plt.subplot(1,2,1)
plt.scatter(x.Petal_Length, x.Petal_Width, c=colormap[model2.predict(x)], s=40)
plt.title('EM Classification')
plt.show()

print("Actual target is:\n", iris.target)
print("K Means target is:\n", model.labels_)
print("EM target is:\n", model2.predict(x))
print("Accuracy of K Means is:\n", accuracy_score(y, model.labels_))
print("Confusion Matrix of K Means is:\n", confusion_matrix(y, model.labels_))
print("Accuracy of EM is:\n", accuracy_score(y, model2.predict(x)))
print("Confusion Matrix of EM is:\n", confusion_matrix(y, model2.predict(x)))

