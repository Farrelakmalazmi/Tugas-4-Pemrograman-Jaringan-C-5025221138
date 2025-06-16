from socket import *
import socket
import logging
from concurrent.futures import ThreadPoolExecutor
from http import HttpServer

# Menginisialisasi 'koki utama'
httpserver = HttpServer()

def ProcessTheClient(connection, address):
    """
    Fungsi ini menangani satu klien. Didesain untuk membaca seluruh
    HTTP request sebelum mengirimnya ke http.py untuk diproses.
    """
    full_request_bytes = b''
    try:
        # Loop untuk memastikan seluruh data request diterima
        while True:
            data = connection.recv(1024)
            if not data:
                break
            full_request_bytes += data
            # Cek sederhana untuk akhir request (untuk request tanpa body)
            if full_request_bytes.endswith(b'\r\n\r\n'):
                # Untuk metode yang mungkin punya body (misal: POST), kita perlu logika lebih lanjut
                # Namun, untuk tugas ini, kita asumsikan server menerima data hingga koneksi ditutup klien
                # atau ada timeout. Logika yang lebih andal akan memeriksa Content-Length.
                # Untuk sementara, kita cek apakah ada Content-Length
                if b'Content-Length' not in full_request_bytes:
                    break
            # Jika request memiliki body, kita harus menunggu hingga semua data body diterima.
            # Logika di bawah ini adalah penyederhanaan.
            # Cara yang benar adalah mem-parsing Content-Length dan membaca sejumlah byte tersebut.
            if b"\r\n\r\n" in full_request_bytes:
                 header_part, _ = full_request_bytes.split(b"\r\n\r\n", 1)
                 if b"Content-Length: 0" in header_part or b"POST" not in header_part:
                     break
                 # Jika ada content-length dan bukan POST, kita bisa asumsikan request selesai
                 # Ini adalah heuristik, bukan parser HTTP lengkap.
                 # Kita akan mengandalkan timeout atau penutupan koneksi oleh klien untuk request besar.
                 # Setelah 2 detik tidak ada data, anggap selesai
                 connection.settimeout(0.2)
    except socket.timeout:
        # Timeout berarti tidak ada lagi data yang dikirim, request dianggap lengkap
        pass
    except Exception as e:
        logging.error(f"Error saat menerima data: {e}")
    finally:
        connection.settimeout(None)


    if not full_request_bytes:
        connection.close()
        return

    # Kirim seluruh request ke http.py untuk diproses
    try:
        hasil = httpserver.proses(full_request_bytes.decode('utf-8', errors='ignore'))
        connection.sendall(hasil)
    except Exception as e:
        logging.error(f"Error saat memproses atau mengirim balasan: {e}")
    
    connection.close()
    return

def Server():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    my_socket.bind(('0.0.0.0', 8885))
    my_socket.listen(1)
    # Pesan startup yang jelas
    logging.warning("Server (Thread Pool) aktif dan mendengarkan di port 8885...")

    with ThreadPoolExecutor(20) as executor:
        while True:
            try:
                connection, client_address = my_socket.accept()
                logging.warning(f"Koneksi diterima dari {client_address}")
                executor.submit(ProcessTheClient, connection, client_address)
            except Exception as e:
                logging.error(f"Error saat menerima koneksi: {e}")

def main():
    # Mengatur logging dasar
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - [%(levelname)s] - %(message)s')
    Server()

if __name__ == "__main__":
    main()
