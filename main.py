from pymongo import MongoClient

# Daftar URL koneksi MongoDB
mongo_uris = {
    "1": "mongodb+srv://MongoFwb:arab123@cluster0.x4azcc8.mongodb.net/?retryWrites=true&w=majority",
    "2": "mongodb+srv://dantesbot:wildan18@cluster0.fol5tml.mongodb.net/?retryWrites=true&w=majority"
}

def choose_mongo_uri():
    """Memilih MongoDB URI untuk digunakan."""
    print("Pilih MongoDB URI:")
    for key, uri in mongo_uris.items():
        print(f"{key} - {uri}")
    
    while True:
        choice = input("Pilih nomor URI (1 atau 2): ")
        if choice in mongo_uris:
            return MongoClient(mongo_uris[choice])
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def list_databases(client):
    """Menampilkan semua database yang tersedia dengan pilihan nomor."""
    databases = client.list_database_names()
    print("Daftar database yang tersedia:")
    for i, db_name in enumerate(databases, start=1):
        print(f"{i}. {db_name}")

    # Memilih database berdasarkan nomor
    try:
        db_choice = int(input("Pilih nomor database untuk melihat koleksi atau opsi lain (atau 0 untuk kembali): "))
        if db_choice == 0:
            return
        elif 1 <= db_choice <= len(databases):
            selected_db_name = databases[db_choice - 1]
            handle_database_options(client, selected_db_name)
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
    except ValueError:
        print("Masukkan nomor yang valid.")

def handle_database_options(client, db_name):
    """Menampilkan opsi untuk koleksi atau penghapusan database."""
    while True:
        print(f"\nAnda memilih database: '{db_name}'")
        print("1 - Lihat koleksi")
        print("2 - Hapus database ini")
        print("3 - Kembali")

        choice = input("Pilih opsi (1, 2, 3): ")

        if choice == '1':
            list_collections(client, db_name)
        elif choice == '2':
            delete_database(client, db_name)
            break
        elif choice == '3':
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def list_collections(client, db_name):
    """Menampilkan semua koleksi dalam database yang dipilih dengan pilihan nomor."""
    db = client[db_name]
    collections = db.list_collection_names()
    if collections:
        print(f"Koleksi dalam database '{db_name}':")
        for i, collection_name in enumerate(collections, start=1):
            print(f"{i}. {collection_name}")

        # Memilih koleksi berdasarkan nomor
        try:
            collection_choice = int(input("Pilih nomor koleksi untuk melihat data (atau 0 untuk kembali): "))
            if collection_choice == 0:
                return
            elif 1 <= collection_choice <= len(collections):
                selected_collection_name = collections[collection_choice - 1]
                view_collection(db, selected_collection_name)
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
        except ValueError:
            print("Masukkan nomor yang valid.")
    else:
        print(f"Tidak ada koleksi dalam database '{db_name}'.")

def view_collection(db, collection_name):
    """Menampilkan beberapa dokumen pertama dalam koleksi yang dipilih."""
    collection = db[collection_name]
    documents = collection.find().limit(5)  # Membatasi tampilan ke 5 dokumen pertama
    print(f"Beberapa dokumen dalam koleksi '{collection_name}':")
    for doc in documents:
        print(doc)

def delete_database(client, db_name):
    """Menghapus database yang dipilih."""
    confirm = input(f"Apakah Anda yakin ingin menghapus database '{db_name}'? (ketik 'y' untuk konfirmasi): ")
    if confirm.lower() == 'y':
        client.drop_database(db_name)
        print(f"Database '{db_name}' telah dihapus.")
    else:
        print("Penghapusan database dibatalkan.")

def delete_all_collections(client):
    """Menghapus semua koleksi dalam semua database."""
    databases = client.list_database_names()
    for db_name in databases:
        if db_name not in ['admin', 'local']:  # Biasanya database ini tidak dihapus
            db = client[db_name]
            for collection_name in db.list_collection_names():
                db.drop_collection(collection_name)
            print(f"Semua koleksi dalam database '{db_name}' telah dihapus.")

def create_database(client):
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
        print(f"Database '{db_name}' telah dibuat.")
        print(f"URI koneksi untuk database '{db_name}': {client[db_name].client.address}")

def main():
    """Fungsi utama untuk menampilkan menu dan menangani pilihan pengguna."""
    client = choose_mongo_uri()  # Memilih MongoDB URI saat memulai program

    while True:
        print("\nPilihan:")
        print("1 - Lihat database yang tersedia")
        print("2 - Hapus semua koleksi")
        print("3 - Buat database")
        print("4 - Keluar")

        choice = input("Pilih opsi (1, 2, 3, 4): ")

        if choice == '1':
            list_databases(client)
        elif choice == '2':
            delete_all_collections(client)
        elif choice == '3':
            create_database(client)
        elif choice == '4':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih lagi.")

if __name__ == "__main__":
    main()
