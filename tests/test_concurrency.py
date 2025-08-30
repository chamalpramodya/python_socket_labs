# tests/test_concurrency.py
import subprocess
import time
import threading
import socket
import struct
import sys

SERVER = [sys.executable, "src/threaded_chat_server.py"]

def client_worker(msg, results, index):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 60113))
    payload = msg.encode('utf-8')
    s.sendall(struct.pack('!I', len(payload)) + payload)
    # wait for any broadcast (not strict)
    try:
        length_data = s.recv(4)
        if not length_data:
            results[index] = False
            s.close()
            return
        n = struct.unpack('!I', length_data)[0]
        data = s.recv(n)
        results[index] = True
    except Exception:
        results[index] = False
    s.close()

def test_concurrency_broadcast():
    p = subprocess.Popen(SERVER)
    time.sleep(0.6)
    try:
        n = 6
        threads = []
        results = [False]*n
        for i in range(n):
            t = threading.Thread(target=client_worker, args=(f"hello from {i}", results, i))
            threads.append(t)
            t.start()
            time.sleep(0.05)
        for t in threads:
            t.join(timeout=2)
        assert any(results), "No client received any broadcast"
    finally:
        p.terminate()
        p.wait(timeout=2)
