import numpy as np
from sklearn.ensemble import RandomForestClassifier

features = np.load('Data/Training/features.npy')
labels = np.load('Data/Training/target_label.npy')
training_words = np.load('Data/Training/training_words.npy')

clf_test = RandomForestClassifier(max_depth=10, min_samples_split=10, min_samples_leaf=1)
clf_test = clf_test.fit(features, labels)

test_features = np.load('Data/Testing/test_features.npy')
test_labels = np.load('Data/Testing/test_target_label.npy')
test_words = np.load('Data/Testing/testing_words.npy')

prediction_label = clf_test.predict( test_features )

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
