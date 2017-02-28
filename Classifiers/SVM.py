import numpy as np
from sklearn import svm
from sklearn.model_selection import KFold
from sklearn import tree

features 	  = np.load('Data/Training/features.npy')
labels   	  = np.load('Data/Training/target_label.npy')
training_words    = np.load('Data/Training/training_words.npy')



kf = KFold(n_splits=10)
kf.get_n_splits(features)

avg_precision=0
avg_recall = 0

for train_index,test_index in kf.split(features):
	F_train,F_test = features[train_index],features[test_index]
	L_train,L_test = labels[train_index],labels[test_index]
	clf = svm.SVC()
	clf.fit(F_train,L_train)


	prediction_score = clf.decision_function( F_test )
	min_threshold = 0.98
	
	prediction_label = [1 if y_s > min_threshold else 0 for y_s in prediction_score]


        num_pos_predictions = np.sum ( prediction_label )

	num_correct_pos_predictions = 0.0

	for k in range( len(prediction_label) ):

		if prediction_label[k] == 1 and prediction_label[k] == L_test[k] :

			num_correct_pos_predictions+=1

	precision = (num_correct_pos_predictions*100/num_pos_predictions)

	num_actual_positives = (L_test == 1).sum()
	recall 	  = (num_correct_pos_predictions*100/num_actual_positives)

	avg_precision+=precision
	avg_recall+=recall


avg_precision/=10
avg_recall/=10

f1=2*avg_precision*avg_recall/(avg_recall+avg_precision)

print avg_precision,avg_recall,f1
