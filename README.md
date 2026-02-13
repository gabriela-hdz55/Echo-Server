# Echo-Server
This project implements an echo server in Python using epoll with edge-triggered, non-blocking sockets.

# Requirements
- Operating System: Linux (WSL on Windows also supported)

     - Note: epoll is Linux-specific and won't work on macOS or native Windows
- Python: 3.6 or higher
- No external dependencies: Uses only Python standard library

# How to Use
## Start Server
1. Run "python3 echo_server.py"

## Echo Client
1. Run "python3 echo_client.py <server_ip> <server_port>" after server is started

## Stress Test
1. Run "python3 echo_server.py" in Terminal #1

2. Run "python3 checker.py <server ip> <port number> <# of trials> <# of reads & writes per run> <max bytes at a time> <# of concurrent connections>" in Terminal #2

- Note: After running stress test, wait 30-60 seconds to allow port to clear and restart server
