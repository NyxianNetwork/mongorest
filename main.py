from pymongo import MongoClient

# URL koneksi MongoDB
url = "mongodb+srv://dantesbot:wildan18@cluster0.fol5tml.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url)

def list_databases():
    """Menampilkan semua database dan koleksi yang tersedia."""
    databases = client.list_database_names()
    print("Daftar database yang tersedia:")
    for db_name in databases:
        print(f"- {db_name}")

        # Mengakses database
        db = client[db_name]

        # Menampilkan semua koleksi dalam database
        collections = db.list_collection_names()
        print(f"  Koleksi dalam database '{db_name}':")
        for collection_name in collections:
            print(f"    - {collection_name}")

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
    """Membuat database baru dengan nama yang diminta pengguna."""
    db_name = input("Masukkan nama database baru: ")
    if db_name in client.list_database_names():
        print(f"Database '{db_name}' sudah ada.")
    else:
        db = client[db_name]
        print(f"Database '{db_name}' telah dibuat.")

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
