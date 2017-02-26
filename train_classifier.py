import numpy as np
from sklearn import svm
from sklearn.model_selection import KFold
from sklearn import tree
from sklearn.naive_bayes import GaussianNB


features = np.load('Data/Training/features.npy')
labels   = np.load('Data/Training/target_label.npy')
training_words    = np.load('Data/Training/training_words.npy')




kf = KFold(n_splits=5)
kf.get_n_splits(features)


for train_index,test_index in kf.split(features):
	F_train,F_test = features[train_index],features[test_index]
	L_train,L_test = labels[train_index],labels[test_index]
	clf = svm.SVC( class_weight={0:1,1:1} )
	clf.fit(F_train,L_train)
	prediction_label = clf.predict(F_test)
	num_pos_predictions = ( prediction_label==1 ).sum()

	num_correct_pos_predictions = 0.0

	for k in range( len(prediction_label) ):

		if prediction_label[k] == 1 and prediction_label[k] == L_test[k] :

			num_correct_pos_predictions+=1

	precision = (num_correct_pos_predictions*100/num_pos_predictions)

	num_actual_positives = (L_test == 1).sum()
	recall 	  = (num_correct_pos_predictions*100/num_actual_positives)

	print precision,recall

	"""
	outFile = open('false_negatives.txt','w+')

	for k in range ( len(prediction_label) ):

		if prediction_label[k] == 0 and L_test[k] == 1:

			outFile.write("\n" + training_words[k] + " " )
			for item in features[k]:
				outFile.write("%s," % item)

	break
	"""


"""
for train_index,test_index in kf.split(features):
	F_train,F_test = features[train_index],features[test_index]
	L_train,L_test = labels[train_index],labels[test_index]
	clf = tree.DecisionTreeClassifier()
	clf.fit(F_train,L_train)
	prediction_label = clf.predict(F_test)
	num_pos_predictions = ( prediction_label==1 ).sum()

	num_correct_pos_predictions = 0.0

	for k in range( len(prediction_label) ):

		if prediction_label[k] == 1 and prediction_label[k] == L_test[k] :

			num_correct_pos_predictions+=1

	precision = (num_correct_pos_predictions*100/num_pos_predictions)

	num_actual_positives = (L_test == 1).sum()
	recall 	  = (num_correct_pos_predictions*100/num_actual_positives)

	print precision,recall


for train_index,test_index in kf.split(features):
	F_train,F_test = features[train_index],features[test_index]
	L_train,L_test = labels[train_index],labels[test_index]
	clf = GaussianNB()
	clf.fit(F_train,L_train)
	prediction_label = clf.predict(F_test)
	num_pos_predictions = ( prediction_label==1 ).sum()

	num_correct_pos_predictions = 0.0

	for k in range( len(prediction_label) ):

		if prediction_label[k] == 1 and prediction_label[k] == L_test[k] :

			num_correct_pos_predictions+=1

	precision = (num_correct_pos_predictions*100/num_pos_predictions)

	num_actual_positives = (L_test == 1).sum()
	recall 	  = (num_correct_pos_predictions*100/num_actual_positives)

	print precision,recall


test_features = np.load('test_features.npy')
test_labels   = np.load('test_target_label.npy')
test_words    = np.load('testing_words.npy')


clf = svm.LinearSVC()
clf = clf.fit(features,labels)
prediction_label = clf.predict( test_features )

num_pos_predictions = ( prediction_label==1 ).sum()

num_correct_pos_predictions = 0.0

for k in range( len(prediction_label) ):

	if prediction_label[k] == 1 and prediction_label[k] == test_labels[k] :

		num_correct_pos_predictions+=1

precision = (num_correct_pos_predictions*100/num_pos_predictions)

num_actual_positives = (test_labels == 1).sum()
recall 	  = (num_correct_pos_predictions*100/num_actual_positives)

print precision,recall
"""




