import socket
import subprocess
import time

def test_tcp_echo():
    #start server
    server =subprocess.Popen(["python", "src/echo_server.py"])
    time.sleep(1) #wait fro start
    
    HOST,PORT ='127.0.0.1',60111
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        message ="hello test"
        s.sendall(message.encode())
        data = s.recv(1024)
        assert data.decode() == message
        
    server.terminate