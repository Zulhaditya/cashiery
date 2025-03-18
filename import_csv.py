import csv
from db import get_connection  # Mengimpor fungsi get_connection dari db.py

# Nama file CSV
csv_file = "dataset/product_with_barcode.csv"

# Membuka koneksi ke database menggunakan fungsi get_connection
conn = get_connection()
cursor = conn.cursor()

# Membuka file CSV dan membaca data
with open(csv_file, newline="", encoding="utf-8") as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        # Mengambil data dari CSV
        kode_barcode = int(row["Kode_Barcode"])  # Pastikan Kode_Barcode adalah integer
        nama_produk = row["Nama_Produk"]
        kategori = None  # Kolom kosong
        harga = None  # Kolom kosong
        satuan = None  # Kolom kosong
        stok = None  # Kolom kosong

        # Cek apakah kode_barcode sudah ada di database
        cursor.execute(
            "SELECT kode_barcode FROM produk WHERE kode_barcode = ?", (kode_barcode,)
        )
        if cursor.fetchone() is None:
            # Jika belum ada, masukkan data ke tabel produk
            cursor.execute(
                """
                INSERT INTO produk (kode_barcode, nama, kategori, harga, satuan, stok)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (kode_barcode, nama_produk, kategori, harga, satuan, stok),
            )
        else:
            print(f"Data dengan kode_barcode {kode_barcode} sudah ada, dilewati.")

# Commit perubahan dan menutup koneksi
conn.commit()
conn.close()

print("Data berhasil diimpor ke SQLite.")
