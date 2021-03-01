import os
import socket
import struct

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
        # 要自己定义协议，前四个字节是发送的消息总长度，之后是正文
        msg_len = struct.pack('<I', len(data))
        self.socket.send(msg_len + data)

    def receive(self)->bytes:
        '''接收数据'''
        # 接收4个字节的消息长度
        responce = self.socket.recv(4)
        # unpack()返回的是元组，第一个元素是长度
        msg_len = struct.unpack('<I', responce)[0]
        if msg_len <= 0:
            raise ValueError('No responce')
        else:
            # 接收正文
            responce = self.socket.recv(msg_len)
            responce_decoded = responce.decode('utf-8')
            self.data.append(responce_decoded)
            print("<{}".format(responce_decoded))
            # 返回字节序列形式
            return responce

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

    def chat(self):
        '''开启聊天窗口'''
        END_CHAT = False

        def receive():
            '''接收数据'''
            self.receive()

        def send():
            '''发送数据'''
            msg = input('>')
            if len(msg) == 0:
                raise ValueError('No data to send')
            if END_CHAT:
                raise ValueError('No request')
            else:
                self.send(msg.encode('utf-8'))

        while True:
            try:
                send()
                receive()
            except ValueError:
                print('[*] Chat ended')
                break
