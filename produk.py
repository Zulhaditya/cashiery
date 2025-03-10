import sqlite3
from db import get_connection
from utils import clear_screen
from tabulate import tabulate


def tambah_produk():
    nama = input("Nama produk: ")
    merk = input("Merk produk: ")
    kode = input("Kode produk: ")
    harga = float(input("Harga produk: "))
    satuan = input("Satuan produk: ")

    conn = sqlite3.connect("kasir.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO produk (nama, merk, kode, harga, satuan) VALUES (?, ?, ?, ?, ?)",
        (nama, merk, kode, harga, satuan),
    )
    conn.commit()
    conn.close()
    print("\n ✅ Produk baru berhasil ditambahkan!")


def lihat_produk():
    clear_screen()
    conn = sqlite3.connect("kasir.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produk")
    produk = cursor.fetchall()
    conn.close()

    if produk:
        print("\n 📦 DATA PRODUK 📦")
        print(
            tabulate(
                produk,
                headers=["ID", "Nama", "Merk", "Kode", "Harga", "Satuan"],
                tablefmt="grid",
            )
        )
    else:
        print(" ⚠️ Tidak ada produk dalam database.")


def cari_produk():
    clear_screen()
    keyword = input("\nMasukkan nama, merk, atau kode produk yang ingin dicari: ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM produk WHERE nama LIKE ? OR merk LIKE ? OR kode LIKE ?",
        (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
    )
    produk = cursor.fetchall()
    conn.close()

    if produk:
        print("\n🔎 Produk ditemukan:")
        print(
            tabulate(
                produk,
                headers=["ID", "Nama", "Merk", "Kode", "Harga", "Satuan"],
                tablefmt="grid",
            )
        )
    else:
        print("\n❌ Produk tidak ditemukan.")


def edit_produk():
    clear_screen()
    cari_produk()
    kode = input("\nMasukkan kode produk yang ingin diedit: ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produk WHERE kode = ?", (kode,))
    produk = cursor.fetchone()

    if not produk:
        print("\n❌ Produk tidak ditemukan.")
        conn.close()
        return

    # Input data baru (bisa dikosongkan untuk mempertahankan nilai lama)
    nama_baru = input(f"Nama baru ({produk[1]}): ") or produk[1]
    merk_baru = input(f"Merk baru ({produk[2]}): ") or produk[2]
    harga_baru = input(f"Harga baru ({produk[4]}): ") or produk[4]
    satuan_baru = input(f"Satuan baru ({produk[5]}): ") or produk[5]

    cursor.execute(
        "UPDATE produk SET nama = ?, merk = ?, harga = ?, satuan = ? WHERE kode = ?",
        (nama_baru, merk_baru, harga_baru, satuan_baru, kode),
    )
    conn.commit()
    conn.close()

    print("\n✅ Produk berhasil diperbarui.")


def hapus_produk():
    clear_screen()
    cari_produk()
    kode = input("\nMasukkan kode produk yang ingin dihapus: ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produk WHERE kode = ?", (kode,))
    produk = cursor.fetchone()

    if not produk:
        print("\n❌ Produk tidak ditemukan.")
        conn.close()
        return

    confirm = (
        input(f"\nApakah Anda yakin ingin menghapus {produk[1]} (Y/N)? ")
        .strip()
        .lower()
    )
    if confirm != "y":
        print("\nHapus produk dibatalkan.")
        conn.close()
        return

    cursor.execute("DELETE FROM produk WHERE kode = ?", (kode,))
    conn.commit()
    conn.close()

    print("\n✅ Produk berhasil dihapus.")
