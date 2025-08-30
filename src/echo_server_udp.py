import socket

HOST ='127.0.0.1'  #LOCALHOST
PORT = 60001 

with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
    s.bind((HOST,PORT))
    print(f"UDP server listening on {HOST}:{PORT}")
    
    while True:
        data, addr = s.recvfrom(1024) 
        print(f"received {data} from {addr}")
        s.sendto(data,addr)
        
        