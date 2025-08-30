import socket   # import the schoke module to use OS's networking api

HOST ='127.0.0.1'   # localhost loopback interface if need other machinse use 0.0.0.0
PORT = 62000    # USE ANYTHING above 1024

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:     # socket.socket() is also fine if want can declare this soc as 1pv4 and TCP stream ased 
    print("socket is created ")
    s.bind((HOST,PORT)) # attach the socket to specified ip and port
                        # if we skip this os pick random port but server need to know the port to connect client 
    s.listen()          # put the socket into listening mode waiting for connection
    print(f"Server listening on {HOST}:{PORT}")  # take a log what server is doing
    
    conn, addr= s.accept()  #Block until a client connects 
                            #conn = new sock obj for that client
                            #addr = clients addr(ip, port)
    with conn:
        print(f"Connected by {addr}")
        while True:                   # allowing mult messages in one conn
            data = conn.recv(1024)    # to read up to 1024
            if not data:              # if the client close the connection recv returns empty --> break the loop
                break
            conn.sendall(data)        # sends th e same data back (echo)
            
        
    

''' Server sets up a mailbox (bind).

Puts a sign saying “I’m open for clients” (listen).

A client knocks → server opens the door (accept), gets a private conversation channel (conn).

Inside the conversation, they exchange letters (send, recv).

When the client leaves, the channel closes.'''
