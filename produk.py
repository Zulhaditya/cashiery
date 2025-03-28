import sqlite3
from db import get_connection
from utils import clear_screen
from tabulate import tabulate
from tambah_barcode import tambah_barcode
from cari_barcode import cari_barcode

def tambah_produk():
    clear_screen()
    print("1. Scan Barcode")
    print("2. Input Manual")
    pilihan = input("Pilih Metode: ")

    if pilihan == "1":
        # Panggil fungsi scan_barcode untuk mendapatkan kode barcode
        kode_barcode = tambah_barcode()
        if kode_barcode is None:
            print("Tidak ada barcode yang terdeteksi atau barcode sudah ada di database.")
            return
    elif pilihan == "2":
        # Input kode barcode secara manual
        kode_barcode = input("Masukkan Kode Barcode: ")
        # Cek apakah kode barcode sudah ada di database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produk WHERE kode_barcode = ?", (kode_barcode,))
        if cursor.fetchone():
            print("Produk dengan kode barcode tersebut sudah ada.")
            conn.close()
            return
        conn.close()
    else:
        print("Pilihan tidak valid.")
        return

    # Input data pelengkap secara manual
    print("\n + TAMBAH PRODUK BARU")
    nama = input("Nama produk: ")
    kategori = input("Kategori Produk: ")
    harga_modal = float(input("Harga modal: "))
    harga_jual = float(input("Harga jual: "))
    satuan = input("Satuan produk: ")
    stok = int(input("Stok produk: "))

    # Tambahkan produk ke database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO produk (kode_barcode, nama, kategori, harga_modal, harga_jual, satuan, stok) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (kode_barcode, nama, kategori, harga_modal, harga_jual, satuan, stok),
    )
    conn.commit()
    conn.close()
    print("\n ✅ Produk baru berhasil ditambahkan!")

def lihat_produk():
    clear_screen()
    conn = sqlite3.connect("kasir.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produk LIMIT 10")
    produk = cursor.fetchall()
    conn.close()

    if produk:
        print("\n 📦 DATA PRODUK")
        print(
            tabulate(
                produk,
                headers=["Kode Barcode", "Nama", "Kategori", "Harga Modal", "Harga Jual", "Satuan", "Stok"],
                tablefmt="fancy_grid",
                numalign="right",
                stralign="center"
            )
        )
    else:
        print(" ⚠️ Tidak ada produk dalam database.")

def cari_produk():
    print("1. Cari dengan Barcode")
    print("2. Cari Manual")
    mode = input("Pilih metode: ")
    if mode == "1":
        keyword = cari_barcode()
        if not keyword:
            print("Tidak ada barcode yang terdeteksi.")
            return
    elif mode == "2":
        keyword = input("\nMasukkan nama, kategori, atau kode barcode: ")
    else:
        print("Mode tidak valid.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM produk WHERE nama LIKE ? OR kategori LIKE ? OR kode_barcode LIKE ?",
        (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
    )
    produk = cursor.fetchall()
    conn.close()

    if produk:
        print("\n🔎 Produk ditemukan:")
        print(
            tabulate(
                produk,
                headers=["Kode Barcode", "Nama", "Kategori", "Harga Modal", "Harga Jual", "Satuan", "Stok"],
                tablefmt="fancy_grid",
                numalign="right",
                stralign="center"
            )
        )


def edit_produk():
    clear_screen()
    lihat_produk()
    keyword = input("\nMasukkan nama, merk, atau barcode produk yang ingin diubah: ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM produk WHERE nama LIKE ? OR kategori LIKE ? OR kode_barcode LIKE ?",
        (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
    )
    produk = cursor.fetchall()

    if not produk:
        print("\n❌ Produk tidak ditemukan.")
        conn.close()
        return

    # Jika lebih dari satu hasil ditemukan, tampilkan daftar dengan tabulate
    if len(produk) > 1:
        print("\n🔎 Beberapa produk ditemukan:")
        from tabulate import tabulate
        produk_list = [(p[0], p[1], p[2], p[3], p[4], p[5], p[6]) for p in produk]  # Pastikan format benar
        print(tabulate(produk_list, 
                       headers=["Kode Barcode", "Nama", "Kategori", "Harga", "Satuan", "Stok"], 
                       tablefmt="fancy_grid",
                       numalign="right",
                       stralign="center"
                       ))

        # BELUM SELESAI HARUS BERDASARKAN BARCODE
        pilihan = input("\nMasukkan ID produk yang ingin diedit: ")
        if not pilihan.isdigit():
            print("\n❌ Pilihan tidak valid.")
            conn.close()
            return

        pilihan = int(pilihan)
        produk = next((p for p in produk if p[0] == pilihan), None)

        if not produk:
            print("\n❌ Produk dengan ID tersebut tidak ditemukan.")
            conn.close()
            return
    else:
        produk = produk[0]

    # Ambil kode produk
    kode = produk[3]

    # Input data baru (bisa dikosongkan untuk mempertahankan nilai lama)
    nama_baru = input(f"Nama baru ({produk[1]}): ") or produk[1]
    merk_baru = input(f"Merk baru ({produk[2]}): ") or produk[2]
    harga_baru = input(f"Harga baru ({produk[4]}): ") or produk[4]
    satuan_baru = input(f"Satuan baru ({produk[5]}): ") or produk[5]

    stok_input = input(f"Stok baru ({produk[6]}): ")
    stok_baru = int(stok_input) if stok_input.isdigit() else produk[6]

    # Update produk
    cursor.execute(
        "UPDATE produk SET nama = ?, merk = ?, harga = ?, satuan = ?, stok = ? WHERE kode = ?",
        (nama_baru, merk_baru, harga_baru, satuan_baru, stok_baru, kode),
    )
    conn.commit()
    conn.close()

    print("\n✅ Produk berhasil diperbarui.")


def hapus_produk():
    clear_screen()
    lihat_produk()

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
    
    # Reset ulang ID agar tetap berurutan
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='produk'")  # Reset auto-increment
    cursor.execute("UPDATE produk SET id = (SELECT COUNT(*) FROM produk p2 WHERE p2.id <= produk.id)")
    conn.commit()

    conn.close()
    print("\n✅ Produk berhasil dihapus.")
