from db import get_connection
from utils import clear_screen
from tabulate import tabulate
from produk import lihat_produk


def cari_produk(keyword):
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

    return produk


def transaksi():
    clear_screen()
    lihat_produk()
    print("============ TRANSAKSI ===============")

    conn = get_connection()
    cursor = conn.cursor()

    daftar_produk = []
    total_harga = 0

    while True:
        keyword = input(
            "\nMasukkan kode, nama, atau merk produk (atau ketik 'ok' untuk mengakhiri transaksi): "
        ).strip()
        if keyword.lower() == "ok":
            break

        hasil_pencarian = cari_produk(keyword)

        if not hasil_pencarian:
            print("\n Produk tidak ditemukan. Coba lagi!")
            continue

        print("\n Hasil Pencarian:")
        print(
            tabulate(
                hasil_pencarian,
                headers=["ID", "Nama", "Merk", "Kode", "Harga", "Satuan", "Stok"],
                tablefmt="grid",
            )
        )

        kode_produk = input("\nMasukkan kode produk yang dibeli: ").strip()
        jumlah = int(input("Masukkan jumlah: "))

        # Cek apakah produk ada & stok cukup
        produk = next((p for p in hasil_pencarian if p[3] == kode_produk), None)

        if not produk:
            print("\n Kode produk tidak valid, coba lagi!")
            continue

        if produk[6] < jumlah:
            print("\n Stok tidak mencukupi!")
            continue

        harga_satuan = produk[4]
        subtotal = jumlah * harga_satuan
        total_harga += subtotal

        daftar_produk.append(
            (produk[0], produk[1], kode_produk, jumlah, harga_satuan, subtotal)
        )

    if not daftar_produk:
        print("\n Tidak ada produk yang ditambahkan dalam transaksi.")
        conn.close()
        return

    # Menampilkan ringkasan transaksi sebelum dikonfirmasi
    print("\n📜 Ringkasan Transaksi 📜")
    print(
        tabulate(
            daftar_produk,
            headers=["ID", "Nama", "Kode", "Jumlah", "Harga", "Subtotal"],
            tablefmt="grid",
        )
    )
    print(f"\n💰 Total Harga: Rp {total_harga:,}")

    konfirmasi = input("\nKonfirmasi transaksi? (y/n): ").strip().lower()
    if konfirmasi != "y":
        print("\nTransaksi dibatalkan.")
        conn.close()
        return

    # Input data pelanggan dan metode pembayaran
    pelanggan = input("Nama pelanggan (opsional): ").strip() or None
    kasir = input("Nama kasir (opsional): ").strip() or None
    metode_pembayaran = input(
        "Metode pembayaran (cash, transfer, e-wallet, dll.): "
    ).strip()

    # Simpan transaksi & update stok
    for item in daftar_produk:
        kode_produk, jumlah = item[2], item[3]

        # Kurangi stok produk
        cursor.execute(
            "UPDATE produk SET stok = stok - ? WHERE kode = ?", (jumlah, kode_produk)
        )

        # Simpan transaksi
        cursor.execute(
            """
            INSERT INTO transaksi (kode_produk, jumlah, total_harga, pelanggan, kasir, metode_pembayaran)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (kode_produk, jumlah, item[5], pelanggan, kasir, metode_pembayaran),
        )

        conn.commit()
        conn.close()

        print("\nTransaksi berhasil dicatat!")


def riwayat_transaksi():
    clear_screen()
    conn = get_connection()
    cursor = conn.cursor()

    # Query dengan JOIN untuk mengambil nama produk dari tabel 'produk'
    cursor.execute(
        """
        SELECT t.id, p.nama, t.kode_produk, t.jumlah, t.total_harga, 
               strftime('%d-%m-%Y', t.tanggal), t.pelanggan, t.kasir, t.metode_pembayaran
        FROM transaksi t
        JOIN produk p ON t.kode_produk = p.kode
        ORDER BY t.tanggal DESC
    """
    )

    transaksi = cursor.fetchall()
    conn.close()

    if transaksi:
        headers = [
            "ID",
            "Nama",
            "Kode",
            "Qty",
            "Total",
            "Tanggal",
            "Pelanggan",
            "Kasir",
            "Metode",
        ]
        print("\n📜 RIWAYAT TRANSAKSI 📜")
        print(
            tabulate(
                transaksi,
                headers=headers,
                tablefmt="fancy_grid",
                numalign="right",
                stralign="center",
            )
        )
    else:
        print("\n⚠️ Belum ada transaksi yang dicatat.")
