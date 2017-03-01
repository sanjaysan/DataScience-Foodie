import numpy as np
from sklearn import linear_model
from sklearn.model_selection import KFold

# Training features(x) and labels(y)
x = np.load('../Data/Training/features.npy')
y = np.load('../Data/Training/target_label.npy')

# Initializing the Linear Regression Classifier
clf = linear_model.LinearRegression()
# Setting up 10-fold cross validation
kf = KFold(n_splits=10)

precision, recall = [], []
for train, test in kf.split(x):
    # Fitting the training data on the model
    clf.fit(x[train], y[train])

    # Selecting only those features for which the predicted value is above the threshold 0.705
    predicted_label = [1 if predicted_val > 0.703 else 0 for predicted_val in clf.predict(x[test])]
    num_correct_pos_predictions = 0.0

    # Calculating out the number of positive predictions
    num_pos_predictions = np.sum(predicted_label)
    for i in range(len(predicted_label)):
        # Comparing the predicted label with the test label to find out the number of correct
        # positive predictions
        if predicted_label[i] == 1 and y[test][i] == 1:
            num_correct_pos_predictions += 1

    # Calculating out the number of actual positives
    num_actual_positives = (y[test] == 1).sum()

    # Calculating precision and recall for each fold
    precision.append(((num_correct_pos_predictions / num_pos_predictions) * 100))
    recall.append(((num_correct_pos_predictions / num_actual_positives) * 100))

# Calculating the average precision and recall
average_precision = np.mean(precision)
average_recall = np.mean(recall)

# Calculating the F1 Measure as (2 PR)/ (P + R)
f1 = (2 * average_precision * average_recall) / (average_precision + average_recall)
print "Precision: ", average_precision
print "Recall: ", average_recall
print "F1 Measure: ", f1
