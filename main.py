from pymongo import MongoClient

# URL koneksi MongoDB
url = "mongodb+srv://dantesbot:wildan18@cluster0.fol5tml.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url)

# Nama database yang ingin dihapus
db_name = 'cluster0'

# Mengakses database
db = client[db_name]

# Menghapus semua koleksi
for collection_name in db.list_collection_names():
    db.drop_collection(collection_name)

print(f"Semua koleksi dalam database '{db_name}' telah dihapus.")
