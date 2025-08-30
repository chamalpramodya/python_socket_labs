# tests/test_tcp_framing.py
import subprocess
import time
import socket
import struct
import os
import sys
import signal

SERVER = [sys.executable, "src/server_with_framing.py"]

def recv_exact(sock, size):
    data = b''
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise ConnectionError("closed")
        data += chunk
    return data

def test_tcp_echo_roundtrip():
    # start server
    p = subprocess.Popen(SERVER)
    time.sleep(0.6)  # small delay to let server start

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 60111))
        # send framed message
        msg = "pytest roundtrip"
        payload = msg.encode('utf-8')
        s.sendall(struct.pack('!I', len(payload)) + payload)

        # receive framed echo
        length_data = recv_exact(s, 4)
        resp_len = struct.unpack('!I', length_data)[0]
        resp = recv_exact(s, resp_len).decode('utf-8')
        assert resp == msg
        s.close()
    finally:
        # stop server
        p.terminate()
        p.wait(timeout=2)
