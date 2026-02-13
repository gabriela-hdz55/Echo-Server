import os
import select
import socket

ECHO_PORT = 9999
BUF_SIZE = 4096

def main():
    print("----- Echo Server -----")
    try:
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print ("socket creation failed with error %s" %(err))
        exit(1)
    serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSock.bind(('0.0.0.0', ECHO_PORT))
    serverSock.listen(128)
    serverSock.setblocking(False)

    # Create epoll instance
    epoll = select.epoll()

    # Register server socket for read events
    epoll.register(serverSock.fileno(), select.EPOLLIN | select.EPOLLET)
    connections = {}

    try:
        while True:
            events = epoll.poll() # Blocks until an event occurs
            for fileno, event in events:
                if fileno == serverSock.fileno():
                    while True: # Accept all incoming connections until no more are available
                        try:
                            connection, addr = serverSock.accept()
                            connection.setblocking(False) # Set connection to non-blocking
                            epoll.register(connection.fileno(), select.EPOLLIN | select.EPOLLET) # Notify when sent data
                            connections[connection.fileno()] = connection # keep track of connections
                        except BlockingIOError:
                            break
                else:
                    conn = connections[fileno]
                    data_chunks = []

                    while True: # Read all available data from the socket
                        try:
                            chunk = conn.recv(BUF_SIZE)
                            if not chunk:
                                # Client disconnected
                                epoll.unregister(fileno)
                                conn.close()
                                del connections[fileno]
                                break
                            data_chunks.append(chunk)
                        except BlockingIOError:
                            # No more data
                            break
                    
                    # Echo back everything received
                    if data_chunks:
                        all_data = b''.join(data_chunks)
                        try:
                            conn.sendall(all_data)
                        except Exception as e:
                            print(f"Connection closed")
                            epoll.unregister(fileno)
                            conn.close()
                            del connections[fileno]

    finally:
        epoll.close()
        serverSock.close()

if __name__ == '__main__':
    main()
