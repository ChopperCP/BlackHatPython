import socket
import threading
import os
import struct
import time
import sys


class Session:
    def __init__(self, client_socket:socket):
        self.socket = client_socket
        self.data = []

    def receive(self):
        '''接收数据'''
        # 接收4个字节的消息长度
        request = self.socket.recv(4)

        # print(request)

        # unpack()返回的是元组，第一个元素是长度
        msg_len = struct.unpack('<I', request)[0]
        if msg_len <= 0:
            raise ValueError('No request')
        else:
            # 接收正文
            request = self.socket.recv(msg_len)
            request_decoded = request.decode('utf-8')
            self.data.append(request_decoded)

            print("<{}".format(request_decoded))

            # 返回字节序列形式
            return request

    def send(self, data: bytes):
        '''发送数据'''
        data_len = len(data)
        self.socket.send(struct.pack(
                '<I', data_len) + data)

    def print_data(self):
        '''打印所有收到的信息'''
        print('\tSession {}:{} has received:'.format(*self.addr))
        line_no = 1
        for line in self.data:
            # 行号居左，宽度为4
            print('\t{:<4}| {}'.format(line_no, line))
            line_no += 1

    def close(self):
        print("[-] Session {}:{} closed".format(*self.socket.getsockname()))
        self.socket.close()


class TCPServer:
    def __init__(self, bind_ip='0.0.0.0', port=9999):
        # 创建套接字
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (bind_ip, port)
        # 绑定端口和IP
        self.socket.bind(self.addr)
        self.sessions = []  # 所有接受的Session

    def listen(self, max_connetion=5):
        '''开始监听'''
        self.socket.listen(max_connetion)
        print("[*] Listening on {}:{}".format(*self.addr))

    def chat(self, session:Session):
        '''开启聊天窗口'''
        def send():
                while True:
                    try:
                        msg=input('>')
                        session.send(msg.encode('utf-8'))
                    except:
                        session.close()
                        sys.exit()

        def receive():
            while True:
                try :
                    session.receive()
                except:
                    pass
        send_handler=threading.Thread(target=send)
        send_handler.setDaemon(True)    
        send_handler.start()

        recv_handler=threading.Thread(target=receive)
        recv_handler.setDaemon(True)
        recv_handler.start()
        try:
            #保持主进程活跃不退出
            time.sleep(10000)
        except:
            session.close()
            sys.exit()

    def getfile(self, session: Session):
        try:
            filename = session.receive().decode('utf-8')
            content = session.receive()
        except:
            pass

        print('[*] Received: {}'.format(filename))
        with open(filename, 'wb') as fileobj:
            fileobj.write(content)

    def handle_client(self, client_socket: socket):
        '''开始接受并处理数据'''
        addr, port = client_socket.getsockname()

        # 处理函数
        # self.getfile(session)
        session = Session(client_socket)
        self.chat(session)


    def run(self, max_connection=5):
        self.listen(max_connection)
        # 主循环，接收和发送数据
        while True:
            # 与客户端成功建立连接后，返回一个元组(client_socket,address_information)
            # 其中，address_information是一个元组(address,port)
            cli_sock, cli_addr = self.socket.accept()

            print("[+] Accepted connetion from: {}:{:d}".format(*cli_addr))
            # 挂起线程，处理数据
            cli_handler = threading.Thread(target=self.handle_client, args=(
                cli_sock,))

            cli_handler.setDaemon(True)
            cli_handler.start()

    def print_sessions(self):
        for session in self.sessions:
            session.print_data()
