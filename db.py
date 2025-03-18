import sqlite3

DB_NAME = "kasir.db"


def get_connection():
    # membuka koneksi ke database dan mengembalikan objek koneksi
    return sqlite3.connect(DB_NAME)


# inisialisasi database


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS produk(
            kode_barcode INTEGER PRIMARY KEY,
            nama TEXT NOT NULL,
            kategori TEXT,
            harga_modal FLOAT,
            harga_jual FLOAT,
            satuan TEXT,
            stok INT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transaksi(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barcode_transaksi INT NOT NULL,
            jumlah INTEGER NOT NULL,
            total_harga FLOAT NOT NULL,
            tanggal DATETIME DEFAULT CURRENT_TIMESTAMP,
            pelanggan TEXT,
            kasir TEXT,
            metode_pembayaran TEXT,
            keterangan TEXT,
            FOREIGN KEY (barcode_transaksi) REFERENCES produk(kode_barcode) ON DELETE CASCADE
        )
    """
    )
    conn.commit()
    conn.close()
