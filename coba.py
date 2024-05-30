import pandas as pd

def main():
    # Membaca data dari file CSV
    data = pd.read_csv('dataset.csv')
    
    # Mencetak beberapa baris pertama dan nama kolom untuk debugging
    print("Data Head:\n", data.head())
    print("Nama Kolom:\n", data.columns)

    # Mengekstrak label dan menghapusnya dari data
    if 'Kategori' not in data.columns:
        print("Error: Kolom 'Kategori' tidak ditemukan dalam dataset")
        return
    
    labels = data['Kategori']
    del data['Kategori']

    # Mengubah DataFrame menjadi daftar kamus
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
