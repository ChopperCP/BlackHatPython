import socket
from TCP_client_Class import TCPClient
import os
import threading
# import time

target = input('Please input your target host. ')
# target = '10.0.0.2'
PORT_BEG=1
PORT_END=25000
PORTS = range(PORT_BEG, PORT_END+1)
OPEN_PORTS = []
threads = []


def portscan(host, port, verbose=False):
    global OPEN_PORTS
    client = TCPClient(host, port)
    try:
        client.connect()
    except:
        pass
    else:
        OPEN_PORTS.append(port)
        if verbose:
            print('[*] {}:{} Opened'.format(*client.addr))

    client.close()



print('[+] Scanning {}:{}-{}'.format(target,PORT_BEG,PORT_END))
for port in PORTS:
    thread = threading.Thread(target=portscan, args=(target, port, True))
    thread.start()
    threads.append(thread)


print('[-] Target {} Opened the following port(s)'.format(target))
print('\t' + ' '.join([str(port) for port in OPEN_PORTS]))

os.system('pause')
