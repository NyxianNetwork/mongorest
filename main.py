from pymongo import MongoClient
import psycopg2

# Daftar URL koneksi
mongo_uris = {
    "1": "mongodb+srv://MongoFwb:arab123@cluster0.x4azcc8.mongodb.net/?retryWrites=true&w=majority",
    "2": "mongodb+srv://dantesbot:wildan18@cluster0.fol5tml.mongodb.net/?retryWrites=true&w=majority",
    "3": "mongodb+srv://nydhfile:deckro1@deckro1.yqikogu.mongodb.net/?retryWrites=true&w=majority&appName=deckro1"
}

postgres_uri = "postgres://rqswfcxa:G-zGbJW1dw2NWCkwtqFBUqGs8jpnVf4m@berry.db.elephantsql.com/rqswfcxa"

def choose_database_type():
    """Memilih jenis database (MongoDB atau PostgreSQL)."""
    print("Pilih jenis database:")
    print("1 - MongoDB")
    print("2 - PostgreSQL")
    
    while True:
        choice = input("Pilih nomor jenis database: ")
        if choice == '1':
            return "mongodb"
        elif choice == '2':
            return "postgresql"
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def connect_to_postgresql():
    """Menghubungkan ke database PostgreSQL."""
    try:
        conn = psycopg2.connect(postgres_uri)
        return conn
    except psycopg2.Error as e:
        print(f"Gagal terhubung ke PostgreSQL: {e}")
        return None

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
        print("2 - Pilih PostgreSQL")
        print("3 - Tambah MongoDB URI")
        print("4 - Hapus MongoDB URI")
        print("5 - Keluar")

        choice = input("Pilih opsi (1, 2, 3, 4, 5): ")

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
            conn = connect_to_postgresql()
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
            remove_mongo_uri()
        elif choice == '5':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
