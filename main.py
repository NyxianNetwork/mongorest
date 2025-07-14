from pymongo import MongoClient
import psycopg2

# Daftar URL koneksi MongoDB dan PostgreSQL
mongo_uris = {
    "1": "mongodb+srv://MongoFwb:arab123@cluster0.x4azcc8.mongodb.net/?retryWrites=true&w=majority",
    "2": "mongodb+srv://dantesbot:wildan18@cluster0.fol5tml.mongodb.net/?retryWrites=true&w=majority",
    "3": "mongodb+srv://nydhfile:deckro1@deckro1.yqikogu.mongodb.net/?retryWrites=true&w=majority&appName=deckro1"
}

postgres_uris = {
    "1": "postgres://rqswfcxa:G-zGbJW1dw2NWCkwtqFBUqGs8jpnVf4m@berry.db.elephantsql.com/rqswfcxa"
}

def add_mongo_uri():
    name = input("Masukkan nomor untuk MongoDB URI baru: ")
    uri = input("Masukkan MongoDB URI baru: ")
    mongo_uris[name] = uri
    print(f"MongoDB URI '{uri}' telah ditambahkan dengan nomor '{name}'.")

def remove_mongo_uri():
    name = input("Masukkan nomor untuk MongoDB URI yang akan dihapus: ")
    if name in mongo_uris:
        del mongo_uris[name]
        print(f"MongoDB URI dengan nomor '{name}' telah dihapus.")
    else:
        print("Nomor MongoDB URI tidak ditemukan.")

def choose_mongo_uri():
    print("Pilih MongoDB URI:")
    for key, uri in mongo_uris.items():
        print(f"{key} - {uri}")

    while True:
        choice = input("Pilih nomor URI: ")
        if choice in mongo_uris:
            return MongoClient(mongo_uris[choice])
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def list_databases(client):
    databases = client.list_database_names()
    print("Daftar database yang tersedia:")
    for i, db_name in enumerate(databases, start=1):
        print(f"{i}. {db_name}")

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
    db = client[db_name]
    collections = db.list_collection_names()
    if collections:
        print(f"Koleksi dalam database '{db_name}':")
        for i, collection_name in enumerate(collections, start=1):
            print(f"{i}. {collection_name}")

        try:
            collection_choice = int(input("Pilih nomor koleksi untuk melihat data atau opsi lain (atau 0 untuk kembali): "))
            if collection_choice == 0:
                return
            elif 1 <= collection_choice <= len(collections):
                selected_collection_name = collections[collection_choice - 1]
                handle_collection_options(db, selected_collection_name)
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
        except ValueError:
            print("Masukkan nomor yang valid.")
    else:
        print(f"Tidak ada koleksi dalam database '{db_name}'.")

def handle_collection_options(db, collection_name):
    while True:
        print(f"\nAnda memilih koleksi: '{collection_name}'")
        print("1 - Lihat dokumen")
        print("2 - Edit dokumen")
        print("3 - Ganti semua nilai tertentu")
        print("4 - Kembali")

        choice = input("Pilih opsi (1, 2, 3, 4): ")

        if choice == '1':
            view_collection(db, collection_name)
        elif choice == '2':
            edit_collection(db, collection_name)
        elif choice == '3':
            search_and_replace_value(db, collection_name)
        elif choice == '4':
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def view_collection(db, collection_name):
    collection = db[collection_name]
    page = 0
    limit = 5

    while True:
        skip = page * limit
        documents = list(collection.find().skip(skip).limit(limit))

        if not documents:
            print("\nTidak ada dokumen untuk ditampilkan.")
            break

        print(f"\nMenampilkan halaman {page + 1}:")
        for i, doc in enumerate(documents, start=1 + skip):
            print(f"{i}. {doc}")

        print("\n--- Navigasi ---")
        print("n - Halaman berikutnya")
        print("p - Halaman sebelumnya")
        print("q - Kembali")

        nav = input("Pilih opsi navigasi (n/p/q): ").lower()

        if nav == 'n':
            page += 1
        elif nav == 'p' and page > 0:
            page -= 1
        elif nav == 'q':
            break
        else:
            print("Pilihan tidak valid.")

def edit_collection(db, collection_name):
    collection = db[collection_name]
    query = {}

    print("Masukkan kriteria pencarian dokumen untuk diedit (kosongkan untuk memilih semua dokumen).")
    field = input("Field: ")
    if field:
        value = input(f"Nilai untuk field '{field}': ")
        query[field] = value

    documents = list(collection.find(query))

    if documents:
        print(f"\nDokumen yang ditemukan: {len(documents)}")
        for i, doc in enumerate(documents, start=1):
            print(f"{i}. {doc}")

        try:
            doc_choice = int(input("Pilih nomor dokumen untuk diedit (atau 0 untuk kembali): "))
            if doc_choice == 0:
                return
            elif 1 <= doc_choice <= len(documents):
                selected_doc = documents[doc_choice - 1]
                update_document(collection, selected_doc)
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
        except ValueError:
            print("Masukkan nomor yang valid.")
    else:
        print("Tidak ada dokumen yang ditemukan dengan kriteria tersebut.")

def update_document(collection, document):
    print("\nDokumen yang dipilih untuk diedit:")
    print(document)

    def display_fields(doc, parent_key=''):
        fields = []
        for key, value in doc.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            fields.append(full_key)
            if isinstance(value, dict):
                fields.extend(display_fields(value, full_key))
        return fields

    fields = display_fields(document)

    print("Pilih field yang ingin diubah:")
    for i, field in enumerate(fields, start=1):
        print(f"{i} - {field}")

    try:
        choice = int(input("Pilih opsi (1, 2, 3, ...): "))
        if 1 <= choice <= len(fields):
            field_to_update = fields[choice - 1]
            new_value = input(f"Masukkan nilai baru untuk field '{field_to_update}': ")
            collection.update_one({"_id": document["_id"]}, {"$set": {field_to_update: new_value}})
            print(f"Field '{field_to_update}' telah diperbarui.")
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
    except ValueError:
        print("Masukkan nomor yang valid.")

def search_and_replace_value(db, collection_name):
    collection = db[collection_name]
    field = input("Masukkan nama field yang akan dicari nilainya: ")
    old_value = input(f"Masukkan nilai yang ingin diganti pada field '{field}': ")
    new_value = input(f"Masukkan nilai baru untuk menggantikan '{old_value}': ")

    result = collection.update_many({field: old_value}, {"$set": {field: new_value}})
    print(f"Sebanyak {result.modified_count} dokumen telah diperbarui di koleksi '{collection_name}'.")

def delete_database(client, db_name):
    confirm = input(f"Apakah Anda yakin ingin menghapus database '{db_name}'? (ketik 'y' untuk konfirmasi): ")
    if confirm.lower() == 'y':
        client.drop_database(db_name)
        print(f"Database '{db_name}' telah dihapus.")
    else:
        print("Penghapusan database dibatalkan.")

def delete_all_collections(client):
    databases = client.list_database_names()
    for db_name in databases:
        if db_name not in ['admin', 'local']:
            db = client[db_name]
            for collection_name in db.list_collection_names():
                db.drop_collection(collection_name)
            print(f"Semua koleksi dalam database '{db_name}' telah dihapus.")
    print("Penghapusan semua koleksi selesai.")

def create_database(client):
    db_name = input("Masukkan nama untuk database baru: ")
    db = client[db_name]
    print(f"Database '{db_name}' telah dibuat.")

def main():
    while True:
        print("\nPilihan:")
        print("1 - Pilih MongoDB URI")
        print("2 - Keluar")

        choice = input("Pilih opsi (1, 2): ")

        if choice == '1':
            client = choose_mongo_uri()
            while True:
                print("\nPilihan:")
                print("1 - Lihat database MongoDB yang tersedia")
                print("2 - Hapus semua koleksi MongoDB")
                print("3 - Buat database MongoDB")
                print("4 - Kembali")

                choice = input("Pilih opsi (1, 2, 3, 4): ")

                if choice == '1':
                    list_databases(client)
                elif choice == '2':
                    delete_all_collections(client)
                elif choice == '3':
                    create_database(client)
                elif choice == '4':
                    break
                else:
                    print("Pilihan tidak valid. Silakan coba lagi.")
        elif choice == '2':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
