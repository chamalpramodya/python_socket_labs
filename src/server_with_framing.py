import socket
import struct  # frot packing / unpacking
import time

def recv_exact(sock, size):
    #read excatly 'size' bytes from the socket
    data =b''
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise ConnectionError("client disconnected ")
        data += chunk
    return data

HOST ='127.0.0.1'
PORT = 60111

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((HOST,PORT))
    s.listen()
    print("server listening on",(HOST,PORT))
    
    conn, addr = s.accept()
    with conn:
        print("connected by",addr)
        conn.settimeout(60)
        
        while True:
            try:
                #read 4 bytes length prefix (network byte order/big endian)
                length_data = recv_exact(conn,4)
            except ConnectionError:
                print("client closed connection")
                break
            except socket.timeout:
                print("connection timed out .closing ")
                break
            
            #Unpack message length
            msg_length = struct.unpack('!I',length_data)[0]
            if msg_length == 0:
                #zero length message used as clients wants to quit
                print("received zero length >> cliets wants to quit")
                break
            #read the exact message bytes 
            message_bytes = recv_exact(conn,msg_length)
            message =message_bytes.decode('utf-8',errors='replace')
            print(f"[{time.strftime('%H:%M:%S')}] Received:{message!r}")
            
            #echo back using same framing
            payload =message.encode('utf-8')
            conn.sendall(struct.pack('!I',len(payload))+payload)
    print('server shutting down')        