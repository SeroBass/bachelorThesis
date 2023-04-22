# Data Processing
import sys
import time

import pandas as pd
import numpy as np

# Modelling
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint

# Tree Visualisation
from sklearn.tree import export_graphviz
from IPython.display import Image
import graphviz

def rfc ():
    data = pd.read_csv('data/financials/ml_prepared/master.csv', index_col=0)
    total_count = data.size
    nan_count = int(data.isna().sum().sum())
    print('Total fields: ' + str(total_count))
    print('Amount of nan: ' + str(nan_count))
    print('Percent of nan: ' + str(100/total_count*nan_count))
    print('Replacing nan with 0')
    data = data.fillna(0)

    X = data.drop(['ml_goal_reached', 'ticker', 'target_price', 'price'], axis=1)
    y = data['ml_goal_reached']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)



    rf = RandomForestClassifier(random_state= 42, n_estimators= 100, min_samples_split= 2, min_samples_leaf= 5, max_depth= 5, bootstrap= False)
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    print(confusion_matrix(y_test, y_pred))

    grid_rf = {
        'n_estimators': [100, 200],
        'max_depth': np.arange(1, 15, 1),
        'min_samples_split': [2, 10, 9],
        'min_samples_leaf': np.arange(1, 15, 2, dtype=int),
        'bootstrap': [True, False],
        'random_state': [1, 2, 30, 42]
    }
    rscv = RandomizedSearchCV(estimator=rf, param_distributions=grid_rf, cv=3, n_jobs=-1, verbose=2, n_iter=200)
    rscv_fit = rscv.fit(X_train, y_train)
    best_parameters = rscv_fit.best_params_
    print(best_parameters)







    sys.exit()

    #time.sleep(1000)



    feature_names = list(X.columns)

    x_train, x_test, y_train, y_test = train_test_split(X, y, train_size=0.9, test_size=0.1)

    #scale = StandardScaler()
    #x_train = scale.fit_transform(x_train)
    #x_test = scale.transform(x_test)

    model = RandomForestClassifier()
    model.fit(x_train, y_train)



    y_pred = model.predict(x_test)
    x_col_list = list(X.columns)

    feature_importance_list = list(model.feature_importances_)

    data = {
        'fundamental_data': x_col_list,
        'importance': feature_importance_list
    }

    #abc = (pd.DataFrame(data=data)).sort_values(by=['importance'], ascending=False)
    #print(abc)

    #print(metrics.r2_score(y_test, y_pred))

    #defg = model.decision_path(x_train)
    #print()
    #print(model.feature_importances_)


    #print('https://medium.com/@maryamuzakariya/project-predict-stock-prices-using-random-forest-regression-model-in-python-fbe4edf01664')


