from matplotlib import pyplot as plt
from sklearn import datasets
from sklearn.manifold import TSNE

#Downloading The digits dataset
digits = datasets.load_digits()
# optional print statements
print len(digits['images'])#, digits['target']
# print digits['images'][0].shape

# flattening the 2D Array to 1D Array
flatten = []
for eachDigit in digits['images']:
    temp = []
    for eachrow in eachDigit:
        temp.extend(eachrow)
    flatten.append(temp)

# plotting with t-nse
X_tsne = TSNE(learning_rate=100).fit_transform(flatten)
plt.figure(figsize=(10, 5))
plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=digits['target'])

plt.show()
