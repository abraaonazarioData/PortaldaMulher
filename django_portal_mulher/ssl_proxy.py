import ssl
import socket
import threading
import sys
import os

LISTEN_HOST = '0.0.0.0'
LISTEN_PORT = 443
TARGET_HOST = '127.0.0.1'
TARGET_PORT = 8000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CERT_FILE = os.path.join(BASE_DIR, 'local_cert.crt')
KEY_FILE = os.path.join(BASE_DIR, 'local_cert.key')

def pipe(src, dst):
    try:
        while True:
            data = src.recv(65536)
            if not data:
                break
            dst.sendall(data)
    except Exception:
        pass
    finally:
        try:
            src.close()
        except:
            pass
        try:
            dst.close()
        except:
            pass

def handle_client(client_sock):
    try:
        backend_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_sock.connect((TARGET_HOST, TARGET_PORT))
        t1 = threading.Thread(target=pipe, args=(client_sock, backend_sock), daemon=True)
        t2 = threading.Thread(target=pipe, args=(backend_sock, client_sock), daemon=True)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    except Exception:
        try:
            client_sock.close()
        except:
            pass

def main():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    
    bind_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bind_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    bind_sock.bind((LISTEN_HOST, LISTEN_PORT))
    bind_sock.listen(128)
    print(f"HTTPS proxy listening on {LISTEN_HOST}:{LISTEN_PORT} -> {TARGET_HOST}:{TARGET_PORT}")
    sys.stdout.flush()
    
    with ctx.wrap_socket(bind_sock, server_side=True) as s:
        while True:
            try:
                client_sock, addr = s.accept()
                threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()
            except Exception as e:
                pass

if __name__ == '__main__':
    main()
