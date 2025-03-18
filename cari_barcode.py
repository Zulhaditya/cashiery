import cv2
from pyzbar import pyzbar
import sqlite3
import time


def cari_barcode():
    # Set untuk menyimpan barcode yang sudah terdeteksi
    barcode_terdeteksi = set()

    # Fungsi untuk memeriksa apakah barcode ada di database SQLite
    def cek_barcode_di_database(barcode):
        # Bersihkan barcode yang terdeteksi
        barcode = barcode.strip()

        # Buka koneksi ke database SQLite
        conn = sqlite3.connect("kasir.db")
        cursor = conn.cursor()

        # Cari barcode di database
        cursor.execute("SELECT nama FROM produk WHERE kode_barcode = ?", (barcode,))
        hasil = cursor.fetchone()
        conn.close()

        if hasil:
            return hasil[0]  # Kembalikan nama produk jika ditemukan
        return None  # Kembalikan None jika tidak ditemukan

    # URL kamera HP Android (ganti dengan alamat IP dan port yang sesuai)
    url_kamera_hp = "http://192.168.1.2:8080/video"  # Contoh untuk IP Webcam
    # url_kamera_hp = "http://192.168.1.100:4747/video"  # Contoh untuk DroidCam

    # Inisialisasi kamera HP
    cap = cv2.VideoCapture(url_kamera_hp)

    # Variabel untuk menyimpan waktu terakhir barcode terdeteksi
    waktu_terakhir_terdeteksi = time.time()

    # Inisialisasi variabel nama_produk
    nama_produk = None

    print("Tekan 'q' untuk keluar...")

    while True:
        # Baca frame dari kamera HP
        ret, frame = cap.read()
        if not ret:
            print(
                "Gagal mengambil frame dari kamera HP. Pastikan URL benar dan kamera aktif."
            )
            break

        # Deteksi barcode dari frame
        barcodes = pyzbar.decode(frame)
        if barcodes:
            # Update waktu terakhir barcode terdeteksi
            waktu_terakhir_terdeteksi = time.time()

            for barcode in barcodes:
                # Ambil nilai barcode
                barcode_data = barcode.data.decode("utf-8")

                # Cek apakah barcode sudah pernah terdeteksi
                if barcode_data in barcode_terdeteksi:
                    print("Produk sudah pernah ditambahkan.")
                    continue  # Lewati barcode yang sudah terdeteksi

                # Cek apakah barcode ada di database
                nama_produk = cek_barcode_di_database(barcode_data)
                if nama_produk:
                    # Tambahkan barcode ke set barcode_terdeteksi
                    barcode_terdeteksi.add(barcode_data)

                    # Mainkan bunyi notifikasi
                    # os.system("aplay sound/notification.wav")

                    # Berhenti setelah produk berhasil ditambahkan
                    break
                else:
                    print("Produk tidak ditemukan di database.")

                # Gambar kotak di sekitar barcode
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            # Tampilkan pesan "Silakan Scan Produk..." jika tidak ada barcode terdeteksi selama 5 detik
            if time.time() - waktu_terakhir_terdeteksi > 5:
                print("Silakan Scan Produk...")
                waktu_terakhir_terdeteksi = time.time()  # Reset timer

        # Tampilkan frame
        cv2.imshow("Barcode Scanner (Kamera HP)", frame)

        # Keluar dari loop jika tombol 'q' ditekan atau produk berhasil ditambahkan
        if cv2.waitKey(1) & 0xFF == ord("q") or (nama_produk is not None):
            break

    # Tutup kamera dan jendela OpenCV
    cap.release()
    cv2.destroyAllWindows()

    # Tampilkan semua produk yang berhasil ditambahkan
    print("\nProduk ditemukan:")
    for barcode in barcode_terdeteksi:
        nama_produk = cek_barcode_di_database(barcode)
        print(f"{barcode}: {nama_produk}")

    # Kembalikan barcode yang terdeteksi (jika ada)
    return barcode_terdeteksi
