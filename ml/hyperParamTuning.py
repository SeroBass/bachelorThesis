from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
import pandas as pd


def tune_dtc():
    print('Start Hyperparameter Tuning for Decision Tree Classifier')

    # Load master file, assign the features and split data 90-10
    df_data = pd.read_csv('data/financials/master.csv')
    x = df_data.drop(['ml_goal_reached', 'ticker', 'price'], axis=1)
    y = df_data['ml_goal_reached']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42)

    # Define the decision tree classifier object without parameters (only random state=42)
    dtc = DecisionTreeClassifier(random_state=42)

    # Define the parameter grid and perform grid search cross-validation
    param_grid = {
        'max_depth': [2, 3, 5, 10, 20],
        'min_samples_leaf': [5, 10, 20, 50, 100],
        'criterion': ["gini", "entropy"]
    }
    grid_search = GridSearchCV(estimator=dtc, param_grid=param_grid, cv=4, n_jobs=-1, verbose=1, scoring="accuracy")
    grid_search.fit(x_train, y_train)

    # Save the best parameters and best score as text file
    with open('logs/decision_tree_classifier_parameters.txt', 'w') as f:
        params = grid_search.best_params_
        for key in params:
            text = str(key) + ': ' + str(params[key])
            f.write(text)
            f.write('\n')
