from pymongo import MongoClient

# URL koneksi MongoDB tanpa nama database spesifik
base_url = "mongodb+srv://MongoFwb:arab123@cluster0.x4azcc8.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(base_url)

def list_databases():
    """Menampilkan semua database yang tersedia dengan pilihan nomor."""
    databases = client.list_database_names()
    print("Daftar database yang tersedia:")
    for i, db_name in enumerate(databases, start=1):
        print(f"{i}. {db_name}")

    # Memilih database berdasarkan nomor
    try:
        db_choice = int(input("Pilih nomor database untuk melihat koleksi (atau 0 untuk kembali): "))
        if db_choice == 0:
            return
        elif 1 <= db_choice <= len(databases):
            selected_db_name = databases[db_choice - 1]
            db = client[selected_db_name]

            # Menampilkan semua koleksi dalam database yang dipilih
            collections = db.list_collection_names()
            print(f"Koleksi dalam database '{selected_db_name}':")
            for collection_name in collections:
                print(f"  - {collection_name}")
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
    except ValueError:
        print("Masukkan nomor yang valid.")

def delete_all_collections():
    """Menghapus semua koleksi dalam semua database."""
    databases = client.list_database_names()
    for db_name in databases:
        if db_name not in ['admin', 'local']:  # Biasanya database ini tidak dihapus
            db = client[db_name]
            for collection_name in db.list_collection_names():
                db.drop_collection(collection_name)
            print(f"Semua koleksi dalam database '{db_name}' telah dihapus.")

def create_database():
    """Membuat database baru dengan nama yang diminta pengguna dan menampilkan URI."""
    db_name = input("Masukkan nama database baru: ")
    if db_name in client.list_database_names():
        print(f"Database '{db_name}' sudah ada.")
    else:
        # Membuat database dengan menyertakan koleksi untuk memastikan database dibuat
        db = client[db_name]
        db.test_collection.insert_one({"test": "data"})
        client.drop_database(db_name)  # Hapus database dan koleksi test setelah mendapatkan URI
        # Membangun URI
        new_uri = f"mongodb+srv://dantesbot:wildan18@cluster0.fol5tml.mongodb.net/{db_name}?retryWrites=true&w=majority"
        print(f"Database '{db_name}' telah dibuat.")
        print(f"URI koneksi untuk database '{db_name}': {new_uri}")

def main():
    """Fungsi utama untuk menampilkan menu dan menangani pilihan pengguna."""
    while True:
        print("\nPilihan:")
        print("1 - Lihat database yang tersedia")
        print("2 - Hapus semua koleksi")
        print("3 - Buat database")
        print("4 - Keluar")

        choice = input("Pilih opsi (1, 2, 3, 4): ")

        if choice == '1':
            list_databases()
        elif choice == '2':
            delete_all_collections()
        elif choice == '3':
            create_database()
        elif choice == '4':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih lagi.")

if __name__ == "__main__":
    main()
