# threaded_chat_client.py
import socket
import struct
import threading

HOST = '127.0.0.1'
PORT = 44000

def recv_exact(sock, size):
    data = b''
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise ConnectionError("server disconnected")
        data += chunk
    return data

def listen(s):
    try:
        while True:
            length_data = recv_exact(s, 4)
            n = struct.unpack('!I', length_data)[0]
            data = recv_exact(s, n)
            print("\n[INCOMING]", data.decode('utf-8'))
    except Exception:
        print("Listener exiting")

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    t = threading.Thread(target=listen, args=(s,), daemon=True)
    t.start()
    try:
        while True:
            m = input(">> ")
            if m.lower() == "quit":
                s.sendall(struct.pack('!I', 0))
                break
            s.sendall(struct.pack('!I', len(m.encode('utf-8'))) + m.encode('utf-8'))
    finally:
        s.close()