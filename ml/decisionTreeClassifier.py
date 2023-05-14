import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score, average_precision_score
from sklearn.tree import _tree
import numpy as np


def dtc():
    print('Start Decision Tree Classifier')
    # Load the data into a DataFrame called df_data
    df_data = pd.read_csv('data/financials/master.csv')

    # Assign the features to x and the target variable to y
    x = df_data.drop(['ml_goal_reached', 'ticker', 'price'], axis=1)
    y = df_data['ml_goal_reached']

    # Split the data into training and testing sets with a 80-20 split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42)

    # Define the decision tree classifier object
    clf = DecisionTreeClassifier(criterion='entropy', max_depth=20, min_samples_leaf=5, random_state=42)

    # Fit the classifier to the training data
    clf.fit(x_train, y_train)

    # Make predictions on the training data
    y_train_pred = clf.predict(x_train)

    # Make predictions on the test data
    y_test_pred = clf.predict(x_test)

    # Measures and KPIs
    data = {
        'Train Accuracy': accuracy_score(y_train, y_train_pred),
        'Test Accuracy': accuracy_score(y_test, y_test_pred),
        'Precision': precision_score(y_test, y_test_pred),
        'Recall': recall_score(y_test, y_test_pred),
        'F1': f1_score(y_test, y_test_pred),
        'Confusion Matrix': confusion_matrix(y_test, y_test_pred),
        'ROC AUC': roc_auc_score(y_test, y_test_pred),
        'PR AUC': average_precision_score(y_test, y_test_pred)
    }

    # Save measures/KPIs in text file
    with open('logs/decision_tree_classifier_measures.txt', 'w') as f:
        for key in data:
            text = str(key) + ': ' + str(data[key])
            f.write(text)
            f.write('\n')

    # Extract rules of Decision Tree Classifier
    rules = get_rules(clf, list(x_train.columns), ['1', '-1'])
    i = 1
    with open('logs/decision_tree_classifier_rules.txt', 'w') as f:
        for r in rules:
            if "then class: -1 (proba: 100.0%)" in r and i <= 10:
                f.write(r)
                f.write('\n')
                i = i + 1


def get_rules(tree, feature_names, class_names):
    # Source:
    # https://stackoverflow.com/questions/20224526/how-to-extract-the-decision-rules-from-scikit-learn-decision-tree
    # Date: 30.04.2023, 00:55
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
