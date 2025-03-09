import sqlite3
from db import get_connection
from utils import clear_screen


def tambah_produk():
    nama = input("Nama produk: ")
    merk = input("Merk produk: ")
    kode = input("Kode produk: ")
    harga = float(input("Harga produk: "))
    satuan = input("Satuan produk: ")

    conn = sqlite3.connect("kasir.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produk (nama, merk, kode, harga, satuan) VALUES (?, ?, ?, ?, ?)",
                   (nama, merk, kode, harga, satuan))
    conn.commit()
    conn.close()
    print("\nOK, Produk baru berhasil ditambahkan!")


def lihat_produk():
    clear_screen()
    conn = sqlite3.connect("kasir.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produk")
    produk = cursor.fetchall()
    conn.close()

    print("\n================= DATA PRODUK =========================")
    for p in produk:
        print(f"{p[0]}. {p[1]} - {p[2]} - {p[3]} - Rp.{p[4]} per {p[5]}")

    print("\nData produk masih kosong")


def cari_produk():
    clear_screen()
    lihat_produk()
    keyword = input("\nMasukkan nama / merk / kode produk yang ingin dicari: ")
    conn = sqlite3.connect("kasir.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produk WHERE nama LIKE ? OR merk LIKE ? OR kode LIKE ?",
                   (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    produk = cursor.fetchall()
    conn.close()

    if produk:
        print("\nProduk ditemukan:")
        for p in produk:
            print(f"{p[0]}. {p[1]} - {p[2]} - {p[3]} - Rp.{p[4]} per {p[5]}")
    else:
        print("\nProduk tidak ditemukan")


def edit_produk():
    clear_screen()
    lihat_produk()
    keyword = input(
        "\nMasukkan nama, merk, atau kode produk yang ingin diedit: ")
    conn = sqlite3.connect("kasir.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produk WHERE nama LIKE ? OR merk LIKE ? OR kode LIKE ?",
                   (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    produk = cursor.fetchall()

    if not produk:
        print("\nProduk tidak ditemukan.")
        conn.close()
        return

    # Jika lebih dari satu hasil ditemukan, tampilkan daftar untuk dipilih
    if len(produk) > 1:
        print("\nBeberapa produk ditemukan:")
        for idx, p in enumerate(produk, start=1):
            print(f"{idx}. {p[1]} - {p[2]} - {p[3]} - Rp.{p[4]} per {p[5]}")

        pilihan = input("\nPilih nomor produk yang ingin diedit: ")
        if not pilihan.isdigit() or int(pilihan) < 1 or int(pilihan) > len(produk):
            print("\nPilihan tidak valid.")
            conn.close()
            return
        produk = produk[int(pilihan) - 1]
    else:
        produk = produk[0]

    # Input data baru (bisa dikosongkan untuk mempertahankan nilai lama)
    nama_baru = input(f"Nama baru ({produk[1]}): ") or produk[1]
    merk_baru = input(f"Merk baru ({produk[2]}): ") or produk[2]
    harga_baru = input(f"Harga baru ({produk[4]}): ")
    satuan_baru = input(f"Satuan baru ({produk[5]}): ") or produk[5]

    harga_baru = float(harga_baru) if harga_baru else produk[4]

    cursor.execute("UPDATE produk SET nama = ?, merk = ?, harga = ?, satuan = ? WHERE kode = ?",
                   (nama_baru, merk_baru, harga_baru, satuan_baru, produk[3]))
    conn.commit()
    conn.close()
    print("\nProduk berhasil diperbarui.")


def hapus_produk():
    clear_screen()
    lihat_produk()
    keyword = input(
        "\nMasukkan nama, merk, atau kode produk yang ingin dihapus: ")

    conn = sqlite3.connect("kasir.db")
    cursor = conn.cursor()

    # Cari produk berdasarkan keyword
    cursor.execute("SELECT * FROM produk WHERE nama LIKE ? OR merk LIKE ? OR kode LIKE ?",
                   (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    produk = cursor.fetchall()

    if not produk:
        print("\nProduk tidak ditemukan.")
        conn.close()
        return

    # Jika lebih dari satu produk ditemukan, admin bisa memilih mana yang akan dihapus
    if len(produk) > 1:
        print("\nBeberapa produk ditemukan:")
        for idx, p in enumerate(produk, start=1):
            print(f"{idx}. {p[1]} - {p[2]} - {p[3]} - Rp.{p[4]} per {p[5]}")

        pilihan = input("\nPilih nomor produk yang ingin dihapus: ")
        if not pilihan.isdigit() or int(pilihan) < 1 or int(pilihan) > len(produk):
            print("\nPilihan tidak valid.")
            conn.close()
            return
        produk = produk[int(pilihan) - 1]
    else:
        produk = produk[0]

    # Konfirmasi penghapusan
    confirm = input(f"\nApakah Anda yakin ingin menghapus {
                    produk[1]} (Y/N)? ").strip().lower()
    if confirm != 'y':
        print("\nPenghapusan dibatalkan.")
        conn.close()
        return

    # Hapus produk dari database
    cursor.execute("DELETE FROM produk WHERE kode = ?", (produk[3],))
    conn.commit()

    # Reset ID agar tetap berurutan
    cursor.execute("SELECT * FROM produk ORDER BY id ASC")
    produk_tersisa = cursor.fetchall()

    cursor.execute("DELETE FROM produk")  # Kosongkan tabel
    # Reset autoincrement
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='produk'")

    # Masukkan ulang data dengan ID baru
    for idx, p in enumerate(produk_tersisa, start=1):
        cursor.execute("INSERT INTO produk (id, nama, merk, kode, harga, satuan) VALUES (?, ?, ?, ?, ?, ?)",
                       (idx, p[1], p[2], p[3], p[4], p[5]))

    conn.commit()
    conn.close()
    print("\nProduk berhasil dihapus dan nomor ID telah diperbarui.")
