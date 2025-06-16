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
