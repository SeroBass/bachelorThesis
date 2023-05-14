from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
import pandas as pd

def tune_dtc():
    print('Start Hyperparameter Tuning for Decision Tree Classifier')
    # Load the data into a DataFrame called df_data
    # Assign the features to X and the target variable to y
    df_data = pd.read_csv('data/financials/master.csv')
    X = df_data.drop(['ml_goal_reached', 'ticker', 'price'], axis=1)
    y = df_data['ml_goal_reached']

    # Split the data into training and testing sets with a 80-20 split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define the decision tree classifier object
    dtc = DecisionTreeClassifier(random_state=42)

    # Define the parameter grid to search over
    param_grid = {
        'max_depth': [2, 3, 5, 10, 20],
        'min_samples_leaf': [5, 10, 20, 50, 100],
        'criterion': ["gini", "entropy"]
    }

    # Perform grid search cross-validation
    grid_search = GridSearchCV(estimator=dtc, param_grid=param_grid, cv=4, n_jobs=-1, verbose=1, scoring="accuracy")
    grid_search.fit(X_train, y_train)

    # Print the best parameters and best score
    with open('logs/decision_tree_classifier_parameters.txt', 'w') as f:
        params = grid_search.best_params_
        for key in params:
            text = str(key) + ': ' + str(params[key])
            f.write(text)
            f.write('\n')
