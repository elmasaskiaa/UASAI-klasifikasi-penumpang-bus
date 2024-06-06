import numpy as np
import pandas as pd

# Load the dataset
file_path = 'dataset.csv'  # Assume the CSV file is in the same directory as this script
df = pd.read_csv(file_path)

# Convert categorical data to numerical
df = pd.get_dummies(df, columns=['Kategori'], drop_first=True)

# Convert labels to numerical values
label_map = {'Rendah': 0, 'Sedang': 1, 'Tinggi': 2}
df['Prioritas'] = df['Prioritas'].map(label_map)

# Convert DataFrame to list of lists
dataset = df.values.tolist()

# Calculate Gini Impurity
def gini_impurity(groups, classes):
    n_instances = sum([len(group) for group in groups])
    gini = 0.0
    for group in groups:
        size = len(group)
        if size == 0:
            continue
        score = 0.0
        for class_val in classes:
            p = [row[-1] for row in group].count(class_val) / size
            score += p * p
        gini += (1.0 - score) * (size / n_instances)
    return gini

# Split a dataset
def test_split(index, value, dataset):
    left, right = list(), list()
    for row in dataset:
        if row[index] < value:
            left.append(row)
        else:
            right.append(row)
    return left, right

# Select the best split point for a dataset
def get_split(dataset):
    class_values = list(set(row[-1] for row in dataset))
    b_index, b_value, b_score, b_groups = 999, 999, 999, None
    for index in range(len(dataset[0])-1):
        for row in dataset:
            groups = test_split(index, row[index], dataset)
            gini = gini_impurity(groups, class_values)
            if gini < b_score:
                b_index, b_value, b_score, b_groups = index, row[index], gini, groups
    return {'index': b_index, 'value': b_value, 'groups': b_groups}

# Create a terminal node
def to_terminal(group):
    outcomes = [row[-1] for row in group]
    return max(set(outcomes), key=outcomes.count)

# Create child splits for a node or make terminal
def split(node, max_depth, min_size, depth):
    left, right = node['groups']
    del(node['groups'])
    if not left or not right:
        node['left'] = node['right'] = to_terminal(left + right)
        return
    if depth >= max_depth:
        node['left'], node['right'] = to_terminal(left), to_terminal(right)
        return
    if len(left) <= min_size:
        node['left'] = to_terminal(left)
    else:
        node['left'] = get_split(left)
        split(node['left'], max_depth, min_size, depth+1)
    if len(right) <= min_size:
        node['right'] = to_terminal(right)
    else:
        node['right'] = get_split(right)
        split(node['right'], max_depth, min_size, depth+1)

# Build a decision tree
def build_tree(train, max_depth, min_size):
    root = get_split(train)
    split(root, max_depth, min_size, 1)
    return root

# Print a decision tree
def print_tree(node, depth=0):
    if isinstance(node, dict):
        print('%s[X%d < %.3f]' % ((depth*' ', (node['index']+1), node['value'])))
        print_tree(node['left'], depth+1)
        print_tree(node['right'], depth+1)
    else:
        print('%s[%s]' % ((depth*' ', node)))

# Make a prediction with a decision tree
def predict(node, row):
    if row[node['index']] < node['value']:
        if isinstance(node['left'], dict):
            return predict(node['left'], row)
        else:
            return node['left']
    else:
        if isinstance(node['right'], dict):
            return predict(node['right'], row)
        else:
            return node['right']

# Build the tree
tree = build_tree(dataset, 3, 1)

# Print the tree
print_tree(tree)

# Function to map user input to appropriate encoded format
def encode_input(usia, kategori, kehamilan):
    kategori_map = {'Dewasa': [0, 0, 0], 'Ibu Hamil': [1, 0, 0], 'Lansia': [0, 1, 0], 'Remaja': [0, 0, 1]}
    kategori_encoded = kategori_map[kategori]
    return [usia, kehamilan] + kategori_encoded

# Input data from user
usia = int(input("Masukkan usia: "))
kategori = input("Masukkan kategori (Ibu Hamil, Lansia, Remaja, Dewasa): ")
kehamilan = 0
if kategori == 'Ibu Hamil':
    kehamilan = int(input("Masukkan jumlah kehamilan (bulan): "))

# Encode input data
row = encode_input(usia, kategori, kehamilan)

# Make prediction
prediction = predict(tree, row)
label_reverse_map = {0: 'Rendah', 1: 'Sedang', 2: 'Tinggi'}
print(f'Prediction: {label_reverse_map[prediction]}')
