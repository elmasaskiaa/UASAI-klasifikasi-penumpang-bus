import pandas as pd
from math import log2

class Node:
    def __init__(self, attribute=None, threshold=None, left=None, right=None, value=None):
        self.attribute = attribute
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

    def classify(self, instance):
        if self.value is not None:
            return self.value
        if instance[self.attribute] <= self.threshold:
            return self.left.classify(instance)
        else:
            return self.right.classify(instance)

def calculate_entropy(labels):
    total = len(labels)
    counts = {label: labels.count(label) for label in set(labels)}
    return -sum((count/total) * log2(count/total) for count in counts.values())

def split_data(data, labels, attribute, threshold):
    left, right = [], []
    left_labels, right_labels = [], []
    for i in range(len(data)):
        if data[i][attribute] <= threshold:
            left.append(data[i])
            left_labels.append(labels[i])
        else:
            right.append(data[i])
            right_labels.append(labels[i])
    return left, right, left_labels, right_labels

def best_split(data, labels, attributes):
    base_entropy = calculate_entropy(labels)
    best_info_gain, best_split = 0, None
    for attribute in attributes:
        values = set(instance[attribute] for instance in data)
        for value in values:
            left, right, left_labels, right_labels = split_data(data, labels, attribute, value)
            if not left or not right:
                continue
            p_left, p_right = len(left) / len(data), len(right) / len(data)
            info_gain = base_entropy - (p_left * calculate_entropy(left_labels) + p_right * calculate_entropy(right_labels))
            if info_gain > best_info_gain:
                best_info_gain, best_split = info_gain, (attribute, value)
    return best_split

def build_tree(data, labels, attributes):
    if len(set(labels)) == 1:
        return Node(value=labels[0])
    if not attributes:
        return Node(value=max(set(labels), key=labels.count))
    split = best_split(data, labels, attributes)
    if not split:
        return Node(value=max(set(labels), key=labels.count))
    attribute, threshold = split
    left, right, left_labels, right_labels = split_data(data, labels, attribute, threshold)
    left_subtree = build_tree(left, left_labels, attributes)
    right_subtree = build_tree(right, right_labels, attributes)
    return Node(attribute, threshold, left_subtree, right_subtree)

def convert_categorical_to_numeric(data):
    mapping = {'Ibu Hamil': 0, 'Lansia': 1, 'Remaja': 2, 'Dewasa': 3}
    for instance in data:
        instance['Kategori'] = mapping[instance['Kategori']]
    return data

def main():
    # Read data from CSV file
    data = pd.read_csv('dataset.csv')

    # Extract labels and delete them from data
    labels = data['Kategori']
    del data['Kategori']

    # Convert DataFrame to list of dictionaries
    data = data.to_dict(orient='records')

    data = convert_categorical_to_numeric(data)
    attributes = ['Usia', 'Kategori', 'Kehamilan']
    tree = build_tree(data, labels, attributes)

    while True:
        print("\nMasukkan data baru untuk klasifikasi (ketik 'stop' untuk selesai):")
        usia = input("Usia: ")
        if usia.lower() == 'stop':
            break
        try:
            usia = int(usia)
        except ValueError:
            print("Usia harus berupa angka. Silakan coba lagi.")
            continue

        if 0 <= usia < 18:
            kategori = 'Remaja'
        elif 18 <= usia < 60:
            kategori = 'Dewasa'
        elif usia >= 60:
            kategori = 'Lansia'

        if kategori == 'Lansia':
            print("Klasifikasi: Lansia, Prioritas: Tinggi")
            continue
        elif kategori == 'Remaja':
            print("Klasifikasi: Remaja, Prioritas: Rendah")
            continue

        kehamilan = 0
        if kategori == 'Ibu Hamil':
            kehamilan = input("Kehamilan (bulan): ")
            if kehamilan.lower() == 'stop':
                break
            try:
                kehamilan = int(kehamilan)
            except ValueError:
                print("Kehamilan harus berupa angka. Silakan coba lagi.")
                continue

        new_data = {'Usia': usia, 'Kategori': kategori, 'Kehamilan': kehamilan}
        new_data = convert_categorical_to_numeric([new_data])[0]
        result = tree.classify(new_data)
        print(f"Klasifikasi: {result}")

if __name__ == "__main__":
    main()
