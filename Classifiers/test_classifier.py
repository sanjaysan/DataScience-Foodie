import numpy as np
from sklearn import svm
from sklearn import linear_model

features = np.load('../Data/Training/features.npy')
labels = np.load('../Data/Training/target_label.npy')
training_words = np.load('../Data/Training/training_words.npy')

# clf_test = svm.SVC()
clf_test = linear_model.LinearRegression()
clf_test = clf_test.fit(features, labels)

test_features = np.load('../Data/Testing/test_features.npy')
test_labels = np.load('../Data/Testing/test_target_label.npy')
test_words = np.load('../Data/Testing/testing_words.npy')

# prediction_score = clf_test.decision_function(test_features)
prediction_label = clf_test.predict(test_features)
min_threshold = 0.63

prediction_label = [1 if y_s > min_threshold else 0 for y_s in prediction_label]

num_pos_predictions = np.sum(prediction_label)

num_correct_pos_predictions = 0.0

for k in range(len(prediction_label)):

    if prediction_label[k] == 1 and prediction_label[k] == test_labels[k]:
        num_correct_pos_predictions += 1

precision = (num_correct_pos_predictions * 100 / num_pos_predictions)

num_actual_positives = (test_labels == 1).sum()
recall = (num_correct_pos_predictions * 100 / num_actual_positives)

f1 = (2 * precision * recall) / (precision + recall)

print precision, recall, f1
