import socket

ECHO_PORT = 9999
BUF_SIZE = 4096

def main():
    print("----- Echo Server -----")
    try:
        serverSock = socket.socket()
    except socket.error as err:
        print ("socket creation failed with error %s" %(err))
        exit(1)
    serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSock.bind(('0.0.0.0', ECHO_PORT))
    serverSock.listen(5)

    while True:
        connection, addr = serverSock.accept()
        data = connection.recv(BUF_SIZE)
        if not data:
            connection.close()
            continue            
        connection.send(data)
        connection.close()
    serverSock.close()

if __name__ == '__main__':
    main()
