import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score
from sklearn import metrics
from sklearn.tree import export_text
from sklearn import tree
from dtreeviz import dtreeviz # will be used for tree visualization
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.tree import _tree
from sklearn import datasets

import numpy as np

import FundamentalAnalysis as fa

def rfr ():
    data = pd.read_csv('data/financials/ml_prepared/A2A.MI.csv', index_col=0)
    total_count = data.size
    nan_count = int(data.isna().sum().sum())
    print('Total fields: ' + str(total_count))
    print('Amount of nan: ' + str(nan_count))
    print('Percent of nan: ' + str(100/total_count*nan_count))
    print('Replacing nan with 0')
    data = data.fillna(0)

    x = data.drop(['ml_goal_reached', 'ticker', 'target_price', 'price'], axis=1)
    y = data['ml_goal_reached']

    feature_names = list(x.columns)

    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.9, test_size=0.1)

    scale = StandardScaler()
    x_train = scale.fit_transform(x_train)
    x_test = scale.transform(x_test)

    model = RandomForestRegressor()
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    x_col_list = list(x.columns)

    feature_importance_list = list(model.feature_importances_)

    data = {
        'fundamental_data': x_col_list,
        'importance': feature_importance_list
    }

    abc = (pd.DataFrame(data=data)).sort_values(by=['importance'], ascending=False)

    print(metrics.r2_score(y_test, y_pred))

    defg = model.decision_path(x_train)
    hij = model.estimators_
    klm = hij[0]

    #print(hij[0])
    #print(model.feature_importances_)


    #print('https://medium.com/@maryamuzakariya/project-predict-stock-prices-using-random-forest-regression-model-in-python-fbe4edf01664')


