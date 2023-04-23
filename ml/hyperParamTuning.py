from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
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
        'max_depth': [2, 4, 6, 8],
        'min_samples_split': [2, 4, 6, 8],
        'min_samples_leaf': [1, 2, 3, 4],
        'random_state': [1, 2, 30, 42]
    }

    print('Start Hyperparameter Tuning')
    # Perform grid search cross-validation
    grid_search = GridSearchCV(dtc, param_grid, cv=5)
    grid_search.fit(X_train, y_train)

    # Print the best parameters and best score
    print("Best parameters: ", grid_search.best_params_)
    print("Best score: ", grid_search.best_score_)