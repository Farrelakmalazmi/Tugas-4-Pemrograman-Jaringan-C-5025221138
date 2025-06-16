# Tugas 4 : HTTP Server dengan Manajemen File & Konkurensi

Repositori ini berisi implementasi dari sebuah HTTP server yang telah dimodifikasi, dibuat sebagai bagian dari tugas mata kuliah **Praktikum Pemrograman Jaringan (Kelas C)**.

**Disusun oleh:**
- **Nama:** Farrel Akmalazmi Nugraha
- **NRP:** 5025221138

---

## Deskripsi Tugas

Proyek ini mengambil sebuah basis kode HTTP server dan menambahkan fungsionalitas baru untuk manajemen file. Server ini mampu melayani beberapa klien secara bersamaan (*concurrently*) dan dapat dijalankan dalam dua mode: **Thread Pool** dan **Multiprocess**.

### Fitur Utama
Server ini sekarang mendukung tiga operasi file utama melalui metode HTTP:
1.  **Melihat Daftar File (`GET /`)**: Menampilkan seluruh file dan direktori di folder utama server.
2.  **Upload File (`POST /<nama_file>`)**: Mengizinkan klien untuk mengunggah file baru ke server.
3.  **Hapus File (`DELETE /<nama_file>`)**: Mengizinkan klien untuk menghapus file yang ada di server.

### Arsitektur dan Desain
Modifikasi dilakukan dengan pendekatan modular, memisahkan logika HTTP dari logika penanganan koneksi:
-   **`http.py`**: Bertindak sebagai "otak" server. Semua logika untuk memproses request `GET`, `POST`, dan `DELETE` terpusat di sini.
-   **`server_thread_pool_http.py`**: Bertindak sebagai "mesin" yang menggunakan model *Thread Pool* untuk menangani banyak koneksi. Cocok untuk tugas yang bersifat *I/O-bound*.
-   **`server_process_pool_http.py`**: Bertindak sebagai "mesin" alternatif yang menggunakan model *Multiprocessing*. Arsitektur diubah menjadi satu proses per koneksi untuk stabilitas maksimum.
-   **`client.py`**: Sebuah klien interaktif berbasis menu yang dibuat untuk memudahkan pengujian semua fitur baru.

---

## Cara Menjalankan

### 1. Prasyarat
- Python 3
- Sebuah file untuk diunggah (misal: `file_untuk_diupload.txt`)

### 2. Menjalankan Server
Pilih salah satu mode server dan jalankan di terminal:

**Mode Thread Pool (Port 8885):**
```bash
python3 server_thread_pool_http.py
```

**Mode Multiprocess (Port 8889):**
```bash
python3 server_process_pool_http.py
```

### 3. Menjalankan Klien
Buka terminal baru dan jalankan klien interaktif. Pastikan variabel `SERVER_HOST` dan `SERVER_PORT` di dalam `client.py` sudah sesuai dengan server yang Anda jalankan.
```bash
python3 client.py
```
Ikuti menu yang ditampilkan untuk berinteraksi dengan server.

---

## Bukti Pengujian Konkurensi (2 Klien)

Pengujian dilakukan dengan dua klien yang berjalan simultan untuk membuktikan kemampuan server menangani koneksi secara bersamaan.

### 1. Skenario Pengujian dengan Server Mode Thread Pool

<details>
<summary><strong>Klik untuk melihat log lengkap pengujian Thread Pool</strong></summary>

**Log dari Terminal Server:**
```log
(base) jovyan@66869b99047e:~/work/progjar/progjar5$ python3 server_thread_pool_http.py
2025-06-16 10:41:14,831 - [WARNING] - Server (Thread Pool) aktif dan mendengarkan di port 8885...
2025-06-16 10:41:27,372 - [WARNING] - Koneksi diterima dari ('172.16.16.102', 56028)
2025-06-16 10:41:27,373 - [WARNING] - Request Diterima: GET / HTTP/1.1
2025-06-16 10:41:29,488 - [WARNING] - Koneksi diterima dari ('172.16.16.103', 53540)
2025-06-16 10:41:29,488 - [WARNING] - Request Diterima: GET / HTTP/1.1
2025-06-16 10:41:53,695 - [WARNING] - Koneksi diterima dari ('172.16.16.102', 56216)
2025-06-16 10:41:53,695 - [WARNING] - Request Diterima: POST /file_client_1.txt HTTP/1.1
2025-06-16 10:41:53,696 - [WARNING] - File file_client_1.txt berhasil di-upload.
2025-06-16 10:41:56,913 - [WARNING] - Koneksi diterima dari ('172.16.16.103', 52280)
2025-06-16 10:41:56,913 - [WARNING] - Request Diterima: GET / HTTP/1.1
2025-06-16 10:42:22,235 - [WARNING] - Koneksi diterima dari ('172.16.16.102', 40120)
2025-06-16 10:42:22,235 - [WARNING] - Request Diterima: DELETE /file_client_1.txt HTTP/1.1
2025-06-16 10:42:22,235 - [WARNING] - File file_client_1.txt berhasil dihapus.
2025-06-16 10:42:24,497 - [WARNING] - Koneksi diterima dari ('172.16.16.103', 53386)
2025-06-16 10:42:24,498 - [WARNING] - Request Diterima: GET / HTTP/1.1
```

**Log dari Terminal Klien 1:**
```log
--- MENU KLIEN HTTP ---
Pilih Opsi (1-4): 1
[INFO] Meminta daftar file dari server...
--- RESPON DITERIMA ---
...
Daftar File di Server:
...
--- MENU KLIEN HTTP ---
Pilih Opsi (1-4): 2
Masukkan nama file lokal yang akan di-upload (misal: mydocument.txt): file_client_1.txt
[INFO] Meng-upload 'file_client_1.txt' sebagai 'file_client_1.txt'...
--- RESPON DITERIMA ---
HTTP/1.1 201 Created
File file_client_1.txt berhasil dibuat.
--- MENU KLIEN HTTP ---
Pilih Opsi (1-4): 3
Masukkan nama file di server yang akan dihapus: file_client_1.txt
[INFO] Menghapus file 'file_client_1.txt' dari server...
--- RESPON DITERIMA ---
HTTP/1.1 200 OK
File file_client_1.txt berhasil dihapus.
--- MENU KLIEN HTTP ---
Pilih Opsi (1-4): 4
Terima kasih, program keluar.
```

**Log dari Terminal Klien 2:**
```log
--- MENU KLIEN HTTP ---
Pilih Opsi (1-4): 1
[INFO] Meminta daftar file dari server...
--- RESPON DITERIMA ---
... (Daftar file awal) ...
--- MENU KLIEN HTTP ---
Pilih Opsi (1-4): 1
[INFO] Meminta daftar file dari server...
--- RESPON DITERIMA ---
... (Daftar file SETELAH Klien 1 upload, 'file_client_1.txt' muncul) ...
--- MENU KLIEN HTTP ---
Pilih Opsi (1-4): 1
[INFO] Meminta daftar file dari server...
--- RESPON DITERIMA ---
... (Daftar file SETELAH Klien 1 hapus, 'file_client_1.txt' hilang) ...
--- MENU KLIEN HTTP ---
Pilih Opsi (1-4): 4
Terima kasih, program keluar.
```
</details>

### 2. Skenario Pengujian dengan Server Mode Multiprocess

<details>
<summary><strong>Klik untuk melihat log lengkap pengujian Multiprocess</strong></summary>

**Log dari Terminal Server:**
```log
(base) jovyan@66869b99047e:~/work/progjar/progjar5$ python3 server_process_pool_http.py
2025-06-16 10:47:49,959 - [SERVER] - Server (Multiprocess) aktif dan mendengarkan di port 8889...
2025-06-16 10:47:57,401 - [SERVER] - Koneksi diterima dari ('172.16.16.103', 53000)
2025-06-16 10:47:57,408 - [SERVER] - Mulai menangani ('172.16.16.103', 53000)
2025-06-16 10:47:59,410 - [SERVER] - Request Diterima: GET / HTTP/1.1
2025-06-16 10:47:59,411 - [SERVER] - Selesai, koneksi dengan ('172.16.16.103', 53000) ditutup.
2025-06-16 10:48:00,195 - [SERVER] - Koneksi diterima dari ('172.16.16.102', 48928)
... (dan seterusnya, menunjukkan semua operasi berhasil) ...
```

**Log dari Terminal Klien 1 & 2:**
*(Hasil interaksi pada klien identik dengan pengujian Thread Pool, membuktikan fungsionalitas server konsisten di kedua mode.)*
</details>

---

## Kode Sumber Inti

<details>
<summary><strong>`http.py`</strong></summary>

```python
import sys
import os
import uuid
from glob import glob
from datetime import datetime
import logging

class HttpServer:
    def __init__(self):
        self.sessions = {}
        self.types = {}
        self.types['.pdf'] = 'application/pdf'
        self.types['.jpg'] = 'image/jpeg'
        self.types['.png'] = 'image/png'
        self.types['.txt'] = 'text/plain'
        self.types['.html'] = 'text/html'

    def response(self, kode=404, message='Not Found', messagebody=b'', headers={}):
        tanggal = datetime.now().strftime('%c')
        resp = []
        resp.append(f"HTTP/1.1 {kode} {message}\r\n")
        resp.append(f"Date: {tanggal}\r\n")
        resp.append("Connection: close\r\n")
        resp.append("Server: myserver/1.0\r\n")
        
        if not isinstance(messagebody, bytes):
            messagebody = str(messagebody).encode('utf-8')
            
        resp.append(f"Content-Length: {len(messagebody)}\r\n")
        for kk in headers:
            resp.append(f"{kk}: {headers[kk]}\r\n")
        resp.append("\r\n")

        response_headers = "".join(resp)
        response = response_headers.encode('utf-8') + messagebody
        return response

    def proses(self, data):
        requests = data.split("\r\n")
        baris = requests[0]
        
        logging.warning(f"Request Diterima: {baris}")

        j = baris.split(" ")
        try:
            method = j[0].upper().strip()
            object_address = j[1].strip()
            
            headers = {}
            body_start_index = -1
            for i, line in enumerate(requests[1:]):
                if line == '':
                    body_start_index = i + 2
                    break
                parts = line.split(":", 1)
                if len(parts) == 2:
                    headers[parts[0].strip()] = parts[1].strip()
            
            body = ""
            if body_start_index != -1:
                body = "\r\n".join(requests[body_start_index:])

            if method == 'GET':
                return self.http_get(object_address, headers)
            elif method == 'POST':
                return self.http_post(object_address, headers, body)
            elif method == 'DELETE':
                return self.http_delete(object_address, headers)
            else:
                return self.response(405, 'Method Not Allowed', 'Metode tidak didukung', {})
        except IndexError:
            return self.response(400, 'Bad Request', 'Request tidak valid', {})

    def http_get(self, object_address, headers):
        if object_address == '/':
            try:
                files = sorted(os.listdir('.'))
                
                file_list_text = "Daftar File di Server:\n"
                file_list_text += "----------------------\n"
                
                if not files:
                    file_list_text += "(Direktori kosong)\n"
                else:
                    for i, f in enumerate(files):
                        file_list_text += f"{i + 1}. {f}\n"
                
                return self.response(200, 'OK', file_list_text, {'Content-Type': 'text/plain; charset=utf-8'})
            
            except Exception as e:
                return self.response(500, 'Internal Server Error', f"Tidak bisa membaca direktori: {e}", {})

        object_address_path = object_address.lstrip('/')
        if not os.path.exists(object_address_path):
            return self.response(404, 'Not Found', f'File {object_address_path} tidak ditemukan', {})

        try:
            with open(object_address_path, 'rb') as fp:
                isi = fp.read()
            
            fext = os.path.splitext(object_address_path)[1].lower()
            content_type = self.types.get(fext, 'application/octet-stream')
            
            return self.response(200, 'OK', isi, {'Content-type': content_type})
        except Exception as e:
            return self.response(500, 'Internal Server Error', f"Tidak bisa membaca file: {e}", {})

    def http_post(self, object_address, headers, body):
        filename = object_address.lstrip('/')
        
        if not filename or '..' in filename or '/' in filename:
            return self.response(400, 'Bad Request', 'Nama file tidak valid.', {})

        try:
            with open(filename, 'wb') as f:
                f.write(body.encode('utf-8'))
            logging.warning(f"File {filename} berhasil di-upload.")
            return self.response(201, 'Created', f'File {filename} berhasil dibuat.', {})
        except Exception as e:
            logging.error(f"Gagal meng-upload file: {e}")
            return self.response(500, 'Internal Server Error', f"Gagal saat upload: {e}", {})

    def http_delete(self, object_address, headers):
        filename = object_address.lstrip('/')
        
        if not filename or '..' in filename or '/' in filename:
            return self.response(400, 'Bad Request', 'Nama file tidak valid.', {})
        
        if not os.path.exists(filename):
            return self.response(404, 'Not Found', f'File {filename} tidak ditemukan untuk dihapus.', {})

        try:
            os.remove(filename)
            logging.warning(f"File {filename} berhasil dihapus.")
            return self.response(200, 'OK', f'File {filename} berhasil dihapus.', {})
        except Exception as e:
            logging.error(f"Gagal menghapus file: {e}")
            return self.response(500, 'Internal Server Error', f"Gagal saat menghapus: {e}", {})

if __name__ == "__main__":
    httpserver = HttpServer()
```
</details>

<details>
<summary><strong>`client.py`</strong></summary>

```python
import sys
import socket
import logging
import os

SERVER_HOST = '172.16.16.101' 
SERVER_PORT = 8889           

def send_request(request_string):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_HOST, SERVER_PORT))
        
        logging.warning(f"\n--- MENGIRIM REQUEST ---\n{request_string}")
        sock.sendall(request_string.encode())
        
        response_received = b""
        while True:
            data = sock.recv(1024)
            if not data:
                break
            response_received += data
        
        sock.close()
        logging.warning("--- RESPON DITERIMA ---")
        return response_received.decode(errors='ignore')
        
    except Exception as e:
        logging.error(f"Error: {e}")
        return None

def get_file_list():
    print("\n[INFO] Meminta daftar file dari server...")
    request = f"GET / HTTP/1.1\r\nHost: {SERVER_HOST}\r\n\r\n"
    response = send_request(request)
    if response:
        print(response)

def upload_file():
    local_filepath = input("Masukkan nama file lokal yang akan di-upload (misal: mydocument.txt): ")
    
    if not os.path.exists(local_filepath):
        print(f"[ERROR] File lokal '{local_filepath}' tidak ditemukan.")
        return

    remote_filename = input(f"Masukkan nama file untuk disimpan di server (default: {local_filepath}): ")
    if not remote_filename:
        remote_filename = os.path.basename(local_filepath)

    try:
        with open(local_filepath, 'r') as f:
            content = f.read()
            
        print(f"\n[INFO] Meng-upload '{local_filepath}' sebagai '{remote_filename}'...")
        body = content
        headers = [
            f"POST /{remote_filename} HTTP/1.1",
            f"Host: {SERVER_HOST}",
            f"Content-Type: text/plain",
            f"Content-Length: {len(body)}"
        ]
        request = "\r\n".join(headers) + "\r\n\r\n" + body
        response = send_request(request)
        if response:
            print(response)
            
    except Exception as e:
        print(f"[ERROR] Gagal membaca atau meng-upload file: {e}")

def delete_file():
    filename_to_delete = input("Masukkan nama file di server yang akan dihapus: ")
    if not filename_to_delete:
        print("[ERROR] Nama file tidak boleh kosong.")
        return

    print(f"\n[INFO] Menghapus file '{filename_to_delete}' dari server...")
    request = f"DELETE /{filename_to_delete} HTTP/1.1\r\nHost: {SERVER_HOST}\r\n\r\n"
    response = send_request(request)
    if response:
        print(response)

def main():
    logging.basicConfig(level=logging.WARNING, format='%(message)s')
    
    while True:
        print("\n--- MENU KLIEN HTTP ---")
        print("1. Lihat Daftar File di Server")
        print("2. Upload File ke Server")
        print("3. Hapus File di Server")
        print("4. Keluar")
        choice = input("Pilih Opsi (1-4): ")

        if choice == '1':
            get_file_list()
        elif choice == '2':
            upload_file()
        elif choice == '3':
            delete_file()
        elif choice == '4':
            print("Terima kasih, program keluar.")
            break
        else:
            print("[ERROR] Pilihan tidak valid, silakan coba lagi.")

if __name__ == '__main__':
    main()

```
</details>

<details>
<summary><strong>`server_thread_pool_http.py` (Mesin Thread Pool)</strong></summary>

```python
from socket import *
import socket
import logging
from concurrent.futures import ThreadPoolExecutor
from http import HttpServer

httpserver = HttpServer()

def ProcessTheClient(connection, address):
    full_request_bytes = b''
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            full_request_bytes += data
            if full_request_bytes.endswith(b'\r\n\r\n'):
                if b'Content-Length' not in full_request_bytes:
                    break
            if b"\r\n\r\n" in full_request_bytes:
                 header_part, _ = full_request_bytes.split(b"\r\n\r\n", 1)
                 if b"Content-Length: 0" in header_part or b"POST" not in header_part:
                     break
                 connection.settimeout(0.2)
    except socket.timeout:
        pass
    except Exception as e:
        logging.error(f"Error saat menerima data: {e}")
    finally:
        connection.settimeout(None)


    if not full_request_bytes:
        connection.close()
        return

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
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - [%(levelname)s] - %(message)s')
    Server()

if __name__ == "__main__":
    main()

```
</details>

<details>
<summary><strong>`server_process_pool_http.py` (Mesin Multiprocess)</strong></summary>

```python
import socket
import logging
import multiprocessing
import os
from http import HttpServer

class Worker(multiprocessing.Process):
    """
    Setiap instance dari kelas ini adalah sebuah proses pekerja yang independen,
    dibuat khusus untuk menangani satu koneksi klien.
    """
    def __init__(self, connection, address):
        super().__init__()
        self.connection = connection
        self.address = address
        self.httpserver = HttpServer()

    def run(self):
        logging.basicConfig(level=logging.WARNING, format=f'[WORKER PID:{os.getpid()}] %(message)s')
        logging.warning(f"Mulai menangani {self.address}")
        
        full_request_bytes = b''
        try:
            self.connection.settimeout(2.0)
            while True:
                data = self.connection.recv(1024)
                if not data:
                    break
                full_request_bytes += data
        except socket.timeout:
            pass 
        except Exception as e:
            logging.error(f"Error saat menerima data: {e}")
        finally:
            self.connection.settimeout(None)

        if full_request_bytes:
            try:
                request_str = full_request_bytes.decode('utf-8', errors='ignore')
                hasil = self.httpserver.proses(request_str)
                self.connection.sendall(hasil)
            except Exception as e:
                logging.error(f"Error saat memproses/mengirim: {e}")
        
        self.connection.close()
        logging.warning(f"Selesai, koneksi dengan {self.address} ditutup.")


def main():
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - [SERVER] - %(message)s')
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    my_socket.bind(('0.0.0.0', 8889))
    my_socket.listen(5)
    logging.warning("Server (Multiprocess) aktif dan mendengarkan di port 8889...")

    processes = []
    while True:
        try:
            connection, client_address = my_socket.accept()
            logging.warning(f"Koneksi diterima dari {client_address}")
            
            process = Worker(connection, client_address)
            process.start()
            
            connection.close()
            
            processes.append(process)
            
            processes = [p for p in processes if p.is_alive()]

        except Exception as e:
            logging.error(f"Error di server utama: {e}")

if __name__ == "__main__":
    main()

```
</details>
