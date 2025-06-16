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
