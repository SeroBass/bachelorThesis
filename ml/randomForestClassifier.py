import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split


def rfc ():
    # Load the data into a DataFrame called df_data
    df_data = pd.read_csv('data/financials/master.csv')

    # Assign the features to x and the target variable to y
    x = df_data.drop(['ml_goal_reached', 'ticker', 'price', 'price_target'], axis=1)
    y = df_data['ml_goal_reached']

    # Split the data into training and testing sets with a 80-20 split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42)

    # Define the decision tree classifier object
    clf = RandomForestClassifier(random_state=42)

    # Fit the classifier to the training data
    clf.fit(x_train, y_train)

    # Make predictions on the training data
    y_train_pred = clf.predict(x_train)

    # Make predictions on the test data
    y_test_pred = clf.predict(x_test)

    # Compute the training and test accuracy
    train_accuracy = accuracy_score(y_train, y_train_pred)
    test_accuracy = accuracy_score(y_test, y_test_pred)

    # Print the training and test accuracy
    print("Training Accuracy:", train_accuracy)
    print("Test Accuracy:", test_accuracy)

    #print('https://medium.com/@maryamuzakariya/project-predict-stock-prices-using-random-forest-regression-model-in-python-fbe4edf01664')


