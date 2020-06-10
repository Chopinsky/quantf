from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd


def train(data, real):
    # print(data)

    master = data[['front', 'back']].values
    target = data['spot'].values

    X_train, X_test, y_train, y_test = train_test_split(master, target)

    # print("test matrix:", X_test[:5])
    # print("test result:", y_test)
    # draw(X_train, X_test, y_train, y_test)

    # run knn regressor and return results
    knn = KNeighborsRegressor(n_neighbors=5)
    knn.fit(X_train, y_train)

    KNeighborsRegressor(
        algorithm='auto', leaf_size=30, metric='minkowski',
        metric_params=None, n_neighbors=5, p=4, weights='uniform'
    )

    print("R^2 score: {:.2f}".format(knn.score(X_test, y_test)))

    return knn.predict(real)


def draw(X_train, X_test, y_train, y_test):
    # Look at your training data, create data frame from data in X_train
    x_train_df = pd.DataFrame(X_train, columns=['front', 'back'])

    # create a scatter plot from the data frame, color by y_train
    plt.scatter(x_train_df['front'], x_train_df['back'], s=50, c=y_train, alpha=0.5)
    plt.title('X_Train data colored by y_train')
    plt.xlabel('v_front_month')
    plt.ylabel('v_second_month')

    plt.show()
