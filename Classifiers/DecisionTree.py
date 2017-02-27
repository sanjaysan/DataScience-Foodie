import numpy as np
from sklearn import svm
from sklearn.model_selection import KFold
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

features = np.load('../Data/Training/features.npy')
labels = np.load('../Data/Training/target_label.npy')
training_words = np.load('../Data/Training/training_words.npy')
kf = KFold(n_splits=10)
kf.get_n_splits(features)

#print tree.DecisionTreeClassifier().get_params()

precisionSum =0
recallSum =0
for train_index, test_index in kf.split(features):
    F_train, F_test = features[train_index], features[test_index]
    L_train, L_test = labels[train_index], labels[test_index]
    #	clf = svm.SVC()

    clf = tree.DecisionTreeClassifier(max_depth=8)
    clf.fit(F_train, L_train)

    prediction_label = clf.predict(F_test)

    num_pos_predictions = (prediction_label==1).sum()

    num_correct_pos_predictions = 0.0

    for k in range(len(prediction_label)):

        if prediction_label[k] == 1 and prediction_label[k] == L_test[k]:
            num_correct_pos_predictions += 1

    precision = (num_correct_pos_predictions * 100 / num_pos_predictions)

    num_actual_positives = (L_test == 1).sum()
    recall = (num_correct_pos_predictions * 100 / num_actual_positives)

    print precision, recall
    precisionSum = precisionSum + precision
    recallSum = recallSum + recall

precisionAvg = precisionSum/10
recallAvg = recallSum/10
print "Average Precision: "
print precisionAvg
print "Average Recall: "
print recallAvg

fValue = (2*precisionAvg*recallAvg)/(recallAvg+precisionAvg)
print "fValue: "
print fValue
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
