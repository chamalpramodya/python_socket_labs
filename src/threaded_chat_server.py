import socket
import struct
import threading
import time

HOST = '127.0.0.1'
PORT = 44000

clients = [] # list of conn,addr
clients_lock = threading.Lock()

def recv_exact(sock,size):
    data =b''
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise ConnectionError("client disconnected")
        data += chunk
    return data

def send_framed(sock,text):
    payload = text.encode('utf-8')
    sock.sendall(struct.pack('!I',len(payload))+payload)
    
def broadcast(sender_sock,text):
    with clients_lock:
        for c, _ in list(clients):
            if c is sender_sock:
                continue
            try:
                send_framed(c,text)
            except Exception:
                #send fails remove client
                try :
                    c.close()
                except:
                    pass
                clients.remove((c, _))

def handle_client(conn, addr):
    print("Client handler started for", addr)
    try:
        while True:
            length_data = recv_exact(conn, 4)
            msg_length = struct.unpack('!I', length_data)[0]
            if msg_length == 0:
                break
            msg = recv_exact(conn, msg_length).decode('utf-8', errors='replace')
            stamp = time.strftime('%H:%M:%S')
            text = f"[{stamp}] {addr}: {msg}"
            print("Broadcasting:", text)
            broadcast(conn, text)
    except ConnectionError:
        print("Client disconnected:", addr)
    finally:
        with clients_lock:
            clients.remove((conn, addr))
        try:
            conn.close()
        except:
            pass
        print("Cleaned up", addr)
def serve():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print("Threaded chat server listening on", (HOST, PORT))
        while True:
            conn, addr = s.accept()
            with clients_lock:
                clients.append((conn, addr))
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()

if __name__ == "__main__":
    serve()