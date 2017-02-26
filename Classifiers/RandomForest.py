import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

features = np.load('../Data/Training/features.npy')
labels = np.load('../Data/Training/target_label.npy')
clf = RandomForestClassifier(n_estimators=20)

# 5-fold cross validation to get precision
scores = cross_val_score(clf, features, labels, cv = 5, scoring = 'precision')
print "Precision: ", np.mean(scores)

# 5-fold cross validation to get recall
scores = cross_val_score(clf, features, labels, cv = 5, scoring = 'recall')
print "Recall: ", np.mean(scores)
