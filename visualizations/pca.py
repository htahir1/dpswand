import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import numpy as np

with open('data.csv', 'r') as content_file:
    content = content_file.read()
    raw_data = content.replace('\r', "")
    samples = [sample.split(', ') for sample in raw_data.split('\n')]
    X = np.array(samples, dtype=float)


pca = PCA(n_components=2)
X_r = pca.fit(X).transform(X)

# Percentage of variance explained for each components
print('explained variance ratio (first two components): %s'
      % str(pca.explained_variance_ratio_))

plt.figure()

plt.scatter(X_r[:, :1], X_r[:, 1:2])
plt.legend(loc='best', shadow=False, scatterpoints=1)
plt.title('PCA')


plt.show()