import socket

HOST = '127.0.0.1'
PORT = 60001

with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
    message =b"hello, UDP server"
    s.sendto(message,(HOST,PORT))
    data ,server = s.recvfrom(1024)
    
print(f"received {data} from {server}")