import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.tree import export_text
from sklearn.tree import _tree
import numpy as np

def dtc():
    df_data = pd.read_csv('data/financials/master.csv', index_col=0)

    x = df_data.drop(['ml_goal_reached', 'ticker', 'price', 'price_target'], axis=1)
    y = df_data['ml_goal_reached']

    feature_names = list(x.columns)

    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, test_size=0.2)

    model = DecisionTreeClassifier()

    model = model.fit(x_train,y_train)

    y_pred = model.predict(x_test)

    tree_rules = export_text(model, feature_names=list(x_train.columns))

    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

    print()

    rules = get_rules(model, list(x_train.columns), ['1', '-1'])
    for r in rules:
        if "then class: -1 (proba: 100.0%)" in r:
            print(r)

    #print(metrics.r2_score(y_test, y_pred))

def get_rules(tree, feature_names, class_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    paths = []
    path = []

    def recurse(node, path, paths):

        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = "row['" + feature_name[node] + "']"
            threshold = tree_.threshold[node]
            p1, p2 = list(path), list(path)
            p1 += [f"({name} <= {np.round(threshold, 3)})"]
            recurse(tree_.children_left[node], p1, paths)
            p2 += [f"({name} > {np.round(threshold, 3)})"]
            recurse(tree_.children_right[node], p2, paths)
        else:
            path += [(tree_.value[node], tree_.n_node_samples[node])]
            paths += [path]

    recurse(0, path, paths)

    # sort by samples count
    samples_count = [p[-1][1] for p in paths]
    ii = list(np.argsort(samples_count))
    paths = [paths[i] for i in reversed(ii)]

    rules = []
    for path in paths:
        rule = "if "

        for p in path[:-1]:
            if rule != "if ":
                rule += " and "
            rule += str(p)
        rule += " then "
        if class_names is None:
            rule += "response: " + str(np.round(path[-1][0][0][0], 3))
        else:
            classes = path[-1][0][0]
            l = np.argmax(classes)
            rule += f"class: {class_names[l]} (proba: {np.round(100.0 * classes[l] / np.sum(classes), 2)}%)"
        rule += f" | based on {path[-1][1]:,} samples"
        rules += [rule]

    return rules
