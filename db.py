import sqlite3

DB_NAME = "kasir.db"


def get_connection():
    # membuka koneksi ke database dan mengembalikan objek koneksi
    return sqlite3.connect(DB_NAME)

# inisialisasi database


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produk(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            merk TEXT NOT NULL,
            kode TEXT UNIQUE NOT NULL,
            harga FLOAT NOT NULL,
            satuan TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
