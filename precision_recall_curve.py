import numpy as np
import sklearn.metrics
from matplotlib import pyplot as plt

features = np.load('Data/Training/features.npy')
labels = np.load('Data/Training/target_label.npy')
training_words = np.load('Data/Training/training_words.npy')

clf = sklearn.svm.LinearSVC().fit(features, labels)
decision_values = clf.decision_function(features)

precision, recall, thresholds = sklearn.metrics.precision_recall_curve(labels, decision_values)

min_prcsn = 0.94
min_thrshld = min([thresholds[i] for i in range(len(thresholds)) if precision[i] > min_prcsn])

print min_thrshld

plt.plot(recall, precision)
plt.show()
