import socket
import struct
import time

HOST = '127.0.0.1'
PORT = 60111

def recv_exact(sock, size):
    data = b''
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise ConnectionError("Server closed connection")
        data += chunk
    return data
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(10)  # timeout for connect/recv
    s.connect((HOST, PORT))
    print("Connected to server. Type messages; 'quit' to exit.")

    while True:
        msg = input("MESSAGE: ")
        if msg.lower() == "quit":
            # send zero-length message as graceful shutdown signal
            s.sendall(struct.pack('!I', 0))
            break
        payload = msg.encode('utf-8')
        # Send framed message: length (4 bytes) + payload
        s.sendall(struct.pack('!I', len(payload)) + payload)
      
        # Receive framed response
        length_data = recv_exact(s, 4)
        resp_len = struct.unpack('!I', length_data)[0]
        resp = recv_exact(s, resp_len).decode('utf-8', errors='replace')
        print("Echo:", resp)

    print("Client exiting.")