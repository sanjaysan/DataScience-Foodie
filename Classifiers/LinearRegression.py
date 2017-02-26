import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import KFold

features = np.load('../Data/Training/features.npy')
labels = np.load('../Data/Training/target_label.npy')

kf = KFold(n_splits=5)
kf.get_n_splits(features)

for train_index, test_index in kf.split(features):
    F_train, F_test = features[train_index], features[test_index]
    L_train, L_test = labels[train_index], labels[test_index]
    clf = linear_model.LinearRegression()
    clf.fit(F_train, L_train)
    prediction_label = clf.predict(F_test)
    mean = np.mean( (prediction_label - L_test) ** 2)
    variance = clf.score(F_test, L_test)

    print('Coefficients: \n', clf.coef_)
    # The mean squared error
    print("Mean squared error: %.2f"
          % np.mean((clf.predict(F_test) - L_test) ** 2) )

    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % clf.score(F_test, L_test))

    # # Plot outputs
    # x = np.array(F_test)
    # y = np.array(L_test)
    # print "x size, ysize: ", x.size , y.size
    # plt.scatter(x, y, color='black')
    # plt.plot(F_test, clf.predict(F_test), color='blue',linewidth=3)
    #
    # plt.xticks(())
    # plt.yticks(())
    #
    # plt.show()