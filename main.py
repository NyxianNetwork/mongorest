from pymongo import MongoClient

# URL koneksi MongoDB
url = "mongodb+srv://dantesbot:wildan18@cluster0.fol5tml.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url)

# Menampilkan semua database
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

# Jika ingin menghapus semua koleksi dalam database tertentu
# db_name = 'cluster0'
# db = client[db_name]
# for collection_name in db.list_collection_names():
#     db.drop_collection(collection_name)
# print(f"Semua koleksi dalam database '{db_name}' telah dihapus.")
