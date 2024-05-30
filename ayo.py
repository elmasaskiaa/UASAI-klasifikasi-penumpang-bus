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
    from math import log2
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

def prepare_data():
    data = [
        {'Usia': 25, 'Kategori': 'Ibu Hamil', 'Kehamilan': 6},
        {'Usia': 70, 'Kategori': 'Lansia', 'Kehamilan': 0},
        {'Usia': 15, 'Kategori': 'Remaja', 'Kehamilan': 0},
        {'Usia': 68, 'Kategori': 'Lansia', 'Kehamilan': 0},
        {'Usia': 28, 'Kategori': 'Ibu Hamil', 'Kehamilan': 4},
        {'Usia': 17, 'Kategori': 'Remaja', 'Kehamilan': 0},
        {'Usia': 72, 'Kategori': 'Lansia', 'Kehamilan': 0},
        {'Usia': 16, 'Kategori': 'Remaja', 'Kehamilan': 0},
        {'Usia': 26, 'Kategori': 'Ibu Hamil', 'Kehamilan': 7},
        {'Usia': 65, 'Kategori': 'Lansia', 'Kehamilan': 0},
        {'Usia': 34, 'Kategori': 'Dewasa', 'Kehamilan': 0},
        {'Usia': 31, 'Kategori': 'Dewasa', 'Kehamilan': 0},
        {'Usia': 36, 'Kategori': 'Dewasa', 'Kehamilan': 0},
        {'Usia': 40, 'Kategori': 'Dewasa', 'Kehamilan': 0},
        {'Usia': 22, 'Kategori': 'Dewasa', 'Kehamilan': 0},
    ]
    labels = ['Sedang', 'Tinggi', 'Rendah', 'Tinggi', 'Sedang', 'Rendah', 'Tinggi', 'Rendah', 'Tinggi', 'Tinggi',
              'Rendah', 'Rendah', 'Rendah', 'Rendah', 'Rendah']
    return data, labels

def main():
    data, labels = prepare_data()
    if not data:
        print("Tidak ada data yang tersedia.")
        return

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
            print("Usia harus berupa angka. coba lagi.")
            continue

        if usia <= 17:
            print("Klasifikasi: Remaja, Prioritas: Rendah")
            continue
        elif usia >= 65:
            print("Klasifikasi: Lansia, Prioritas: Tinggi")
            continue

        kategori = input("Kategori (Ibu Hamil/Lansia/Remaja/Dewasa): ").title()
        if kategori.lower() == 'stop':
            break
        if kategori not in ['Ibu Hamil', 'Lansia', 'Remaja', 'Dewasa']:
            print("tidak valid.coba lagi.")
            continue

        kehamilan = 0
        if kategori == 'Ibu Hamil':
            kehamilan = input("Kehamilan (bulan): ")
            if kehamilan.lower() == 'stop':
                break
            try:
                kehamilan = int(kehamilan)
            except ValueError:
                print("Berikan angka kehamilan. Tolong input kembali.")
                continue

            if kehamilan <= 3 or kehamilan >= 7:
                print("Klasifikasi: Ibu Hamil, Prioritas: Tinggi")
                continue
            elif 4 <= kehamilan <= 6:
                print("Klasifikasi: Ibu Hamil, Prioritas: Sedang (Trimester 2)")
                continue

        new_data = {'Usia': usia, 'Kategori': kategori, 'Kehamilan': kehamilan}
        new_data = convert_categorical_to_numeric([new_data])[0]
        result = tree.classify(new_data)
        print(f"Klasifikasi: {result}")

if __name__ == "__main__":
    main()
