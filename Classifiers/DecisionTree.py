import numpy as np
from sklearn import tree
from sklearn.model_selection import KFold

x = np.load('../Data/Training/features.npy')
y = np.load('../Data/Training/target_label.npy')

kf = KFold(n_splits=10)
kf.get_n_splits(x)

precisionSum = 0
recallSum = 0
for train, test in kf.split(x):
    clf = tree.DecisionTreeClassifier(max_depth=8)

    clf.fit(x[train], y[train])

    predicted_label = clf.predict(x[test])

    num_pos_predictions = (predicted_label == 1).sum()

    num_correct_pos_predictions = 0.0
    for i in range(len(predicted_label)):
        if predicted_label[i] == 1 and predicted_label[i] == y[test][i]:
            num_correct_pos_predictions += 1

    num_actual_positives = (y[test] == 1).sum()

    precision = (num_correct_pos_predictions * 100 / num_pos_predictions)
    recall = (num_correct_pos_predictions * 100 / num_actual_positives)

    precisionSum = precisionSum + precision
    recallSum = recallSum + recall

precisionAvg = precisionSum / 10
recallAvg = recallSum / 10
print "Precision: ", precisionAvg
print "Recall: ", recallAvg

f1 = (2 * precisionAvg * recallAvg) / (recallAvg + precisionAvg)
print "fValue: ", f1
# import numpy as np
# from sklearn import svm
# from sklearn.model_selection import KFold
# from sklearn import tree
# from sklearn.naive_bayes import GaussianNB
# import pydotplus
# import os
#
# features = np.load('../Data/Training/features.npy')
# labels = np.load('../Data/Training/target_label.npy')
# training_words = np.load('../Data/Training/training_words.npy')
#
# clf = tree.DecisionTreeClassifier()
# clf = clf.fit(features, labels)
#
# clf.predict(features)
#
# with open("iris.dot", 'w') as f:
#     f = tree.export_graphviz(clf, out_file=f)
