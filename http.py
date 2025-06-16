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
