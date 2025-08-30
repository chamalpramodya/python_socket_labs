import socket

HOST ='127.0.0.1'
PORT = 60000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))     #tcp handshake with server
    s.sendall(b'Hello,server') #sends a byte stirng socket only sends bytes not python strings
    data = s.recv(1024)  #waits for sockets response
    print(f"Received {data!r}") #prints the raw repsentation shows the b"
    

'''Client sends: Hello, server → TCP packet.

Server echoes it back.

You can capture this in Wireshark later for evidence.'''