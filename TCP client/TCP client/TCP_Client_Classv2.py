import os
import socket

target_host = "127.0.0.1"  # 目标主机
target_port = 9999  # 目标端口


class TCPClient:
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port
        self.addr = (host, port)  # 元组，地址信息，便于函数拆包使用
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = []  # 已经接收的数据

    def connect(self):
        print('[*] Starting connection {}:{}'.format(*self.addr))
        self.socket.connect(self.addr)
        print('[+] Connected {}:{}'.format(*self.addr))

    def send(self, data: bytes):
        '''向服务器端发送信息'''
        self.socket.send(data)

    def receive(self, buffer=4096)->bytes:
        '''接收信息'''
        response = bytes()  # 所有的数据
        while True:
            data = self.socket.recv(buffer)
            response += data
            if len(data) <= buffer:
                break
        return response

    def print_data(self):
        print('\tConnetion {}:{} has received:'.format(*self.addr))
        line_no = 1
        for line in self.data:
            # 行号居左，宽度为4
            print('\t{:<4}| {}'.format(line_no, line))
            line_no += 1

    def close(self):
        self.socket.close()
        print('[-] Connection {}:{} closed'.format(*self.addr))

client=TCPClient()
client.connect()
client.send('this is a client.'.encode('utf8'))
print(client.receive().decode('utf8'))
client.socket.shutdown()
client.close()