import cv2
from pyzbar import pyzbar
from db import get_connection


def tambah_barcode():
    # URL kamera HP Android (ganti dengan alamat IP dan port yang sesuai)
    url_kamera_hp = "http://192.168.1.2:8080/video"  # Contoh untuk IP Webcam
    cap = cv2.VideoCapture(url_kamera_hp)

    print("Tekan 'q' untuk keluar...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print(
                "Gagal mengambil frame dari kamera HP. Pastikan URL benar dan kamera aktif."
            )
            break

        # Deteksi barcode dari frame
        barcodes = pyzbar.decode(frame)
        if barcodes:
            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8").strip()
                print(f"Barcode Terdeteksi: {barcode_data}")

                # Cek apakah barcode sudah ada di database
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM produk WHERE kode_barcode = ?", (barcode_data,)
                )
                if cursor.fetchone():
                    print("Barcode sudah ada di database. Silakan scan barcode lain.")
                    conn.close()
                else:
                    conn.close()
                    cap.release()
                    cv2.destroyAllWindows()
                    return barcode_data  # Kembalikan kode barcode yang belum ada di database

        # Tampilkan frame
        cv2.imshow("Barcode Scanner (Kamera HP)", frame)

        # Keluar dari loop jika tombol 'q' ditekan
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None  # Kembalikan None jika tidak ada barcode yang terdeteksi
