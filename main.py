import sys
from db import init_db
from produk import tambah_produk, lihat_produk, cari_produk, edit_produk, hapus_produk
from utils import clear_screen


def menu():
    clear_screen()
    while True:
        print("\n================ SELAMAT DATANG DI APLIKASI KASIR ======================")
        print("\nPilihan:")
        print("1. Tambahkan Produk")
        print("2. Lihat Produk")
        print("3. Cari Produk")
        print("4. Edit Produk")
        print("5. Hapus Produk")
        print("6. Keluar")

        pilihan = input("\nPilih [1/2/3/4/5/6]: ")

        if pilihan == '1':
            tambah_produk()
        elif pilihan == '2':
            lihat_produk()
        elif pilihan == '3':
            cari_produk()
        elif pilihan == '4':
            edit_produk()
        elif pilihan == '5':
            hapus_produk()
        elif pilihan == '6':
            print("\nKeluar dari aplikasi ...")
            sys.exit()
        else:
            print("\nPilihan tidak tersedia")


if __name__ == "__main__":
    init_db()
    menu()
