import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold

features = np.load('../Data/Training/features.npy')
labels = np.load('../Data/Training/target_label.npy')
clf = RandomForestClassifier(n_estimators=20)

# # 5-fold cross validation to get precision
# scores = cross_val_score(clf, features, labels, cv = 5, scoring = 'precision')
# print "Precision: ", np.mean(scores)
#
# # 5-fold cross validation to get recall
# scores = cross_val_score(clf, features, labels, cv = 5, scoring = 'recall')
# print "Recall: ", np.mean(scores)
#
# kf = KFold(n_splits=10)
# kf.get_n_splits(features)

kf = KFold(n_splits=10)
kf.get_n_splits(features)
for train_index, test_index in kf.split(features):
    F_train, F_test = features[train_index], features[test_index]
    L_train, L_test = labels[train_index], labels[test_index]
    clf = RandomForestClassifier(n_estimators=20)
    clf.fit(F_train, L_train)

    prediction_score = clf.decision_function(F_test)
    min_threshold = 0.96

    prediction_label = [1 if y_s > min_threshold else 0 for y_s in prediction_score]

    num_pos_predictions = np.sum(prediction_label)

    num_correct_pos_predictions = 0.0

    for k in range(len(prediction_label)):

        if prediction_label[k] == 1 and prediction_label[k] == L_test[k]:
            num_correct_pos_predictions += 1

    precision = (num_correct_pos_predictions * 100 / num_pos_predictions)

    num_actual_positives = (L_test == 1).sum()
    recall = (num_correct_pos_predictions * 100 / num_actual_positives)

    print precision, recall
