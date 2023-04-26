from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
import pandas as pd

def tune_dtc():
    print('Start Hyperparameter Tuning for Decision Tree Classifier')
    # Load the data into a DataFrame called df_data
    # Assign the features to X and the target variable to y
    df_data = pd.read_csv('data/financials/master.csv')
    X = df_data.drop(['ml_goal_reached', 'ticker', 'price', 'price_target'], axis=1)
    y = df_data['ml_goal_reached']

    # Split the data into training and testing sets with a 80-20 split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define the decision tree classifier object
    dtc = DecisionTreeClassifier()

    # Define the parameter grid to search over
    param_grid = {
        'criterion': ['gini', 'entropy'],
        'random_state': [1, 2, 30, 42]
    }

    print('Start Hyperparameter Tuning')
    # Perform grid search cross-validation
    grid_search = GridSearchCV(dtc, param_grid, cv=5)
    grid_search.fit(X_train, y_train)

    # Print the best parameters and best score
    print("Best parameters: ", grid_search.best_params_)
    print("Best score: ", grid_search.best_score_)

def tune_rfc():
    print('Start Hyperparameter Tuning for Random Forest Classifier')
    # Load the data into a DataFrame called df_data
    # Assign the features to X and the target variable to y
    df_data = pd.read_csv('data/financials/master.csv')
    X = df_data.drop(['ml_goal_reached', 'ticker', 'price', 'price_target'], axis=1)
    y = df_data['ml_goal_reached']

    # Split the data into training and testing sets with a 80-20 split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define the parameter grid to search
    param_grid = {
        'n_estimators': [100, 200, 300, 400, 500],
        'max_depth': [5, 10, 15, 20, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['sqrt', 'log2', None],
        'random_state': [1, 2, 30, 42]
    }

    # Create a random forest classifier object
    rfc = RandomForestClassifier()

    # Perform grid search cross validation
    grid_search = GridSearchCV(estimator=rfc, param_grid=param_grid, cv=5)
    grid_search.fit(X_train, y_train)

    # Print the best parameters
    print("Best parameters: ", grid_search.best_params_)