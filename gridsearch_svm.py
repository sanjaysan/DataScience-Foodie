from __future__ import print_function

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC


print(__doc__)

features 	  = np.load('Data/Training/features.npy')
labels   	  = np.load('Data/Training/target_label.npy')
training_words    = np.load('Data/Training/training_words.npy')



F_train,F_test,L_train,L_test = train_test_split( features,labels,test_size=0.5,random_state=0)

tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]


clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=5,
                       scoring='precision_macro')
clf.fit(F_train, L_train)

print("Best parameters set found on development set:")
print()
print(clf.best_params_)
print()
print("Grid scores on development set:")
print()
means = clf.cv_results_['mean_test_score']
stds = clf.cv_results_['std_test_score']
for mean, std, params in zip(means, stds, clf.cv_results_['params']):
    print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))

print()

print("Detailed classification report:")
print()
print("The model is trained on the full development set.")
print("The scores are computed on the full evaluation set.")
print()
L_true, L_pred = L_test, clf.predict(F_test)
print(classification_report(L_true, L_pred))
print()
