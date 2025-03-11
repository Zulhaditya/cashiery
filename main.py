import sys
from db import init_db
from produk import tambah_produk, lihat_produk, cari_produk, edit_produk, hapus_produk
from transaksi import riwayat_transaksi, transaksi
from utils import clear_screen


def menu():
    clear_screen()
    while True:
        print(
            "\n================ SELAMAT DATANG DI APLIKASI KASIR ======================"
        )
        print("\nPilihan:")
        print("1. Menu Transaksi")
        print("2. Riwayat Transaksi")
        print("3. Tambah Produk")
        print("4. Lihat Produk")
        print("5. Cari Produk")
        print("6. Edit Produk")
        print("7. Hapus Produk")
        print("8. Keluar")

        pilihan = input("\nPilih [1/2/3/4/5/6]: ")

        if pilihan == "1":
            transaksi()
        elif pilihan == "2":
            riwayat_transaksi()
        elif pilihan == "3":
            tambah_produk()
        elif pilihan == "4":
            lihat_produk()
        elif pilihan == "5":
            cari_produk()
        elif pilihan == "6":
            edit_produk()
        elif pilihan == "7":
            hapus_produk()
        elif pilihan == "8":
            print("\nKeluar dari aplikasi ...")
            sys.exit()
        else:
            print("\nPilihan tidak tersedia")


if __name__ == "__main__":
    init_db()
    menu()
