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
# ... Tempelkan isi lengkap http.py di sini ...
import sys
import os
# ... (sisa kode)
```
</details>

<details>
<summary><strong>`client.py`</strong></summary>

```python
# ... Tempelkan isi lengkap client.py di sini ...
import sys
import socket
# ... (sisa kode)
```
</details>

<details>
<summary><strong>`server_thread_pool_http.py` (Mesin Thread Pool)</strong></summary>

```python
# ... Tempelkan isi lengkap server_thread_pool_http.py di sini ...
from socket import *
import socket
# ... (sisa kode)
```
</details>

<details>
<summary><strong>`server_process_pool_http.py` (Mesin Multiprocess)</strong></summary>

```python
# ... Tempelkan isi lengkap server_process_pool_http.py di sini ...
import socket
import logging
# ... (sisa kode)
```
</details>
