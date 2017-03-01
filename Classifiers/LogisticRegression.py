import numpy as np
from sklearn import linear_model
from sklearn.model_selection import KFold

# Training features(x) and labels(y)
x = np.load('../Data/Training/features.npy')
y = np.load('../Data/Training/target_label.npy')

# Setting up 10-fold cross validation
kf = KFold(n_splits=10)
kf.get_n_splits(x)

precisionList, recallList = [], []
for train, test in kf.split(x):
    # Initializing the Logistic Regression Classifier
    clf = linear_model.LogisticRegression(class_weight = {0:1, 1:1})
    print clf.get_params(True)

    # Fitting the training data on the model
    clf.fit(x[train], y[train])

    # Running the decision function to find out the predicted score
    prediction_score = clf.decision_function(x[test])

    # Setting the minimum threshold
    min_threshold = 0.96

    # Selecting only those features for which the predicted value is above the minimum threshold
    predicted_label = [1 if y_s > min_threshold else 0 for y_s in prediction_score]

    # Calculating out the number of positive predictions
    num_pos_predictions = np.sum(predicted_label)

    num_correct_pos_predictions = 0.0
    for i in range(len(predicted_label)):
        # Comparing the predicted label with the test label to find out the number of correct
        # positive predictions
        if predicted_label[i] == 1 and predicted_label[i] == y[test][i]:
            num_correct_pos_predictions += 1

    # Calculating out the number of actual positives
    num_actual_positives = (y[test] == 1).sum()

    # Calculating precision and recall for each fold
    precision = (num_correct_pos_predictions * 100 / num_pos_predictions)
    recall = (num_correct_pos_predictions * 100 / num_actual_positives)

    precisionList.append(precision)
    recallList.append(recall)

# Calculating the average precision and recall
average_precision = np.mean(precisionList)
average_recall = np.mean(recallList)
print "Precision: ", average_precision
print "Recall: ", average_recall

# Calculating the F1 Measure as (2 PR)/ (P + R)
f1 = (2 * average_precision * average_recall) / (average_precision + average_recall)
print "F1 Measure: ", f1
