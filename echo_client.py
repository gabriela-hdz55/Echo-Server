import socket
import argparse

ECHO_PORT = 9999
BUF_SIZE = 4096

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="server_ip",action='store', help='server ip')
    parser.add_argument(dest="server_port",action='store', help='server port')
    args = parser.parse_args()

    serverIP = args.server_ip
    try: 
        serverPort = int(args.server_port)
    except ValueError as e:
        print("port number needs to be a valid number")
        exit(1)
    try: 
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    except socket.error as err: 
        print ("socket creation failed with error %s" %(err))

    clientSock.connect((serverIP, serverPort))
    data = input("Please enter the message: ")
    print("Sending ", data)

    message = data.encode()
    clientSock.sendall(message)
    sent_length = len(message)

    recvData = b'' # collection of received data
    while len(recvData) < sent_length:
        chunk = clientSock.recv(BUF_SIZE) # gets data in allowed size
        if not chunk: # no more data
            print("Error: Connection closed before receiving all data")
            exit(1)
        recvData += chunk

    print("Receiving ", recvData.decode()) # data received
    clientSock.close()


if __name__ == '__main__':
    main()
