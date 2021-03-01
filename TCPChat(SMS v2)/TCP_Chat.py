import socket
import threading
import random
import time

local_ip = "172.26.105.246"
local_port = 9999  # only for local test
remote_ip = "172.26.105.246"
remote_port = 10000  # only for local test
client_name = 'ChopperCP'


def server_thread():
    # create server/local socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((local_ip, local_port))  # bind IP and port
    server.listen(1)  # start to listen
    print("[*] Listening at {}:{} ...".format(local_ip, local_port))
    remote, addr = server.accept()
    print("[*] Accepted connection from {}:{}".format(*addr))

    def recv_n_print():
        while True:
            # try:
            msg = remote.recv(4096)
            if msg != b'':
                print(msg.decode('utf8'))
            # except:
            # pass

    handler = threading.Thread(target=recv_n_print)
    handler.start()


def client_thread():
    # create client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((remote_ip, remote_port))
    print("[*]Successfully connected to {}:{} ...".format(remote_ip, remote_port))

    while True:
        msg = input("Message: ")
        msg = '[{}] '.format(client_name)+msg+'\n'
        data = msg.encode('utf8')
        client.send(data)


server = threading.Thread(target=server_thread)
server.start()
# server_thread()
cmd = input("Connect? [Yes/no]")
if cmd == "Yes" or cmd == '':
    client_name = input("Please input your name (for display): ")
    client = threading.Thread(target=client_thread)
    client.start()
