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
