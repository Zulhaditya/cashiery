import sqlite3


def update_table_structure():
    conn = sqlite3.connect("kasir.db")
    cursor = conn.cursor()

    # Ubah nama kolom 'harga' menjadi 'harga_jual'
    cursor.execute("ALTER TABLE produk RENAME COLUMN harga TO harga_jual")

    # Tambahkan kolom 'harga_modal'
    cursor.execute("ALTER TABLE produk ADD COLUMN harga_modal FLOAT")

    conn.commit()
    conn.close()
    print("Struktur tabel berhasil diperbarui.")
