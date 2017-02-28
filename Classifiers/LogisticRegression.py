import numpy as np
from sklearn import linear_model
from sklearn.model_selection import KFold

features = np.load('../Data/Training/features.npy')
labels = np.load('../Data/Training/target_label.npy')
training_words = np.load('../Data/Training/training_words.npy')
kf = KFold(n_splits=10)
kf.get_n_splits(features)

precisionList = []
recallList = []
for train_index, test_index in kf.split(features):
    F_train, F_test = features[train_index], features[test_index]
    L_train, L_test = labels[train_index], labels[test_index]

    clf = linear_model.LogisticRegression()
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

    precisionList.append(precision)
    recallList.append(recall)

print "Precision: ", np.mean(precisionList)
print "Recall: ", np.mean(recallList)

fValue = (2 * np.mean(precisionList) * np.mean(recallList)) / (np.mean(recallList) + np.mean(precisionList))
print "fValue: ", fValue
