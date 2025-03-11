import sqlite3
from db import get_connection
from utils import clear_screen
from tabulate import tabulate

def generate_kode_produk():
    conn = get_connection()
    cursor = conn.cursor()

    # Ambil kode produk terakhir
    cursor.execute("SELECT kode FROM produk ORDER BY id DESC LIMIT 1")
    last_code = cursor.fetchone()
    conn.close()

    if last_code and last_code[0]:
        last_number = int(last_code[0].split("-")[1])  # Ambil angka setelah "-"
        new_number = last_number + 1
    else:
        new_number = 1  # Jika belum ada produk, mulai dari 1

    return f"P-{new_number:04d}"  # Format jadi 'P-0001', 'P-0002', dst.


def tambah_produk():
    nama = input("Nama produk: ")
    merk = input("Merk produk: ")
    harga = float(input("Harga produk: "))
    satuan = input("Satuan produk: ")
    stok = input("Stok produk: ")

    # Buat kode produk secara otomatis
    kode = generate_kode_produk()

    conn = sqlite3.connect("kasir.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO produk (nama, merk, kode, harga, satuan, stok) VALUES (?, ?, ?, ?, ?, ?)",
        (nama, merk, kode, harga, satuan, stok),
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
                headers=["ID", "Nama", "Merk", "Kode", "Harga", "Satuan", "Stok"],
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
                headers=["ID", "Nama", "Merk", "Kode", "Harga", "Satuan", "Stok"],
                tablefmt="grid",
            )
        )
    else:
        print("\n❌ Produk tidak ditemukan.")


def edit_produk():
    clear_screen()
    lihat_produk()
    keyword = input("\nMasukkan nama, merk, atau kode produk yang ingin dicari: ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM produk WHERE nama LIKE ? OR merk LIKE ? OR kode LIKE ?",
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
        print(tabulate(produk_list, headers=["ID", "Nama", "Merk", "Kode", "Harga", "Satuan", "Stok"], tablefmt="grid"))

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
