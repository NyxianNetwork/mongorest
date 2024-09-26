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
    """Menambahkan MongoDB URI ke daftar."""
    name = input("Masukkan nomor untuk MongoDB URI baru: ")
    uri = input("Masukkan MongoDB URI baru: ")
    mongo_uris[name] = uri
    print(f"MongoDB URI '{uri}' telah ditambahkan dengan nomor '{name}'.")

def remove_mongo_uri():
    """Menghapus MongoDB URI dari daftar."""
    name = input("Masukkan nomor untuk MongoDB URI yang akan dihapus: ")
    if name in mongo_uris:
        del mongo_uris[name]
        print(f"MongoDB URI dengan nomor '{name}' telah dihapus.")
    else:
        print("Nomor MongoDB URI tidak ditemukan.")

def choose_mongo_uri():
    """Memilih MongoDB URI untuk digunakan."""
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
    """Menampilkan semua database yang tersedia dengan pilihan nomor."""
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
    """Menampilkan opsi untuk melihat, mengedit, atau mengganti semua nilai dalam koleksi yang dipilih."""
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
    """Menampilkan beberapa dokumen pertama dalam koleksi yang dipilih."""
    collection = db[collection_name]
    documents = collection.find().limit(5)
    print(f"Beberapa dokumen dalam koleksi '{collection_name}':")
    for doc in documents:
        print(doc)

def edit_collection(db, collection_name):
    """Mengedit dokumen dalam koleksi yang dipilih."""
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
    """Memperbarui field dalam dokumen yang dipilih secara fleksibel, termasuk nested fields."""
    print("\nDokumen yang dipilih untuk diedit:")
    print(document)

    # Fungsi rekursif untuk menavigasi dan menampilkan semua fields, termasuk nested fields
    def display_fields(doc, parent_key=''):
        fields = []
        for key, value in doc.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            fields.append(full_key)
            if isinstance(value, dict):
                fields.extend(display_fields(value, full_key))  # Rekursif jika field adalah dict
        return fields

    fields = display_fields(document)  # Mendapatkan semua fields, termasuk nested fields

    print("Pilih field yang ingin diubah:")
    for i, field in enumerate(fields, start=1):
        print(f"{i} - {field}")

    try:
        choice = int(input("Pilih opsi (1, 2, 3, ...): "))
        if 1 <= choice <= len(fields):
            field_to_update = fields[choice - 1]
            new_value = input(f"Masukkan nilai baru untuk field '{field_to_update}': ")
            
            # Menggunakan dot notation untuk update nested fields
            collection.update_one({"_id": document["_id"]}, {"$set": {field_to_update: new_value}})
            print(f"Field '{field_to_update}' telah diperbarui.")
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
    except ValueError:
        print("Masukkan nomor yang valid.")

def search_and_replace_value(db, collection_name):
    """Mencari dan mengganti semua nilai tertentu dalam seluruh database."""
    collection = db[collection_name]
    field = input("Masukkan nama field yang akan dicari nilainya: ")
    old_value = input(f"Masukkan nilai yang ingin diganti pada field '{field}': ")
    new_value = input(f"Masukkan nilai baru untuk menggantikan '{old_value}': ")

    result = collection.update_many({field: old_value}, {"$set": {field: new_value}})

    print(f"Sebanyak {result.modified_count} dokumen telah diperbarui di koleksi '{collection_name}'.")

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
    print("Penghapusan semua koleksi selesai.")

def create_database(client):
    """Membuat database baru dengan nama yang diberikan pengguna."""
    db_name = input("Masukkan nama untuk database baru: ")
    db = client[db_name]
    print(f"Database '{db_name}' telah dibuat.")

def add_postgres_uri():
    """Menambahkan PostgreSQL URI ke daftar."""
    name = input("Masukkan nomor untuk PostgreSQL URI baru: ")
    uri = input("Masukkan PostgreSQL URI baru: ")
    postgres_uris[name] = uri
    print(f"PostgreSQL URI '{uri}' telah ditambahkan dengan nomor '{name}'.")

def remove_postgres_uri():
    """Menghapus PostgreSQL URI dari daftar."""
    name = input("Masukkan nomor untuk PostgreSQL URI yang akan dihapus: ")
    if name in postgres_uris:
        del postgres_uris[name]
        print(f"PostgreSQL URI dengan nomor '{name}' telah dihapus.")
    else:
        print("Nomor PostgreSQL URI tidak ditemukan.")

def choose_postgres_uri():
    """Memilih PostgreSQL URI untuk digunakan."""
    print("Pilih PostgreSQL URI:")
    for key, uri in postgres_uris.items():
        print(f"{key} - {uri}")
    
    while True:
        choice = input("Pilih nomor URI: ")
        if choice in postgres_uris:
            try:
                conn = psycopg2.connect(postgres_uris[choice])
                return conn
            except psycopg2.Error as e:
                print(f"Gagal terhubung ke PostgreSQL: {e}")
                return None
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def list_postgres_databases(conn):
    """Menampilkan semua tabel dalam database PostgreSQL."""
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cursor.fetchall()
    print("Daftar tabel yang tersedia:")
    for i, table_name in enumerate(tables, start=1):
        print(f"{i}. {table_name[0]}")
    
    try:
        table_choice = int(input("Pilih nomor tabel untuk melihat data atau opsi lain (atau 0 untuk kembali): "))
        if table_choice == 0:
            return
        elif 1 <= table_choice <= len(tables):
            selected_table_name = tables[table_choice - 1][0]
            view_postgres_table_data(conn, selected_table_name)
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
    except ValueError:
        print("Masukkan nomor yang valid.")

def view_postgres_table_data(conn, table_name):
    """Menampilkan data dari tabel PostgreSQL yang dipilih."""
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    print(f"Beberapa data dalam tabel '{table_name}':")
    print(columns)
    for row in rows:
        print(row)

def main():
    """Fungsi utama untuk menampilkan menu dan menangani pilihan pengguna."""
    while True:
        print("\nPilihan:")
        print("1 - Pilih MongoDB URI")
        print("2 - Pilih PostgreSQL URI")
        print("3 - Tambah MongoDB URI")
        print("4 - Tambah PostgreSQL URI")
        print("5 - Hapus MongoDB URI")
        print("6 - Hapus PostgreSQL URI")
        print("7 - Keluar")

        choice = input("Pilih opsi (1, 2, 3, 4, 5, 6, 7): ")

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
            conn = choose_postgres_uri()
            if conn:
                while True:
                    print("\nPilihan:")
                    print("1 - Lihat tabel PostgreSQL yang tersedia")
                    print("2 - Kembali")

                    choice = input("Pilih opsi (1, 2): ")

                    if choice == '1':
                        list_postgres_databases(conn)
                    elif choice == '2':
                        conn.close()
                        break
                    else:
                        print("Pilihan tidak valid. Silakan coba lagi.")
        elif choice == '3':
            add_mongo_uri()
        elif choice == '4':
            add_postgres_uri()
        elif choice == '5':
            remove_mongo_uri()
        elif choice == '6':
            remove_postgres_uri()
        elif choice == '7':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
