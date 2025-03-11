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
            satuan TEXT NOT NULL,
            stok INT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaksi(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kode_produk TEXT NOT NULL,
            jumlah INTEGER NOT NULL,
            total_harga FLOAT NOT NULL,
            tanggal DATETIME DEFAULT CURRENT_TIMESTAMP,
            tipe_transaksi TEXT CHECK(tipe_transaksi IN ('penjualan', 'pembelian')) NOT NULL,
            pelanggan TEXT,
            kasir TEXT,
            metode_pembayaran TEXT,
            keterangan TEXT,
            FOREIGN KEY (kode_produk) REFERENCES produk(kode) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()
