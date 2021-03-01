import socket
import threading



class Session:
    def __init__(self, client_socket):
        self.socket = client_socket
        self.data = []

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

        print('>',response.decode('utf8'))
        self.data+=response
        return response

    def print_data(self):
        '''打印所有收到的信息'''
        print('\tSession {}:{} has received:'.format(*self.addr))
        line_no = 1
        for line in self.data:
            # 行号居左，宽度为4
            print('\t{:<4}| {}'.format(line_no, line))
            line_no += 1

    def close(self):
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

    def handle_client(self, client_socket: socket):
        '''开始接受并处理数据'''
        addr, port = client_socket.getsockname()

        # 处理函数
        session=Session(client_socket)

        session.close()
        print("[-] Connection {}:{} closed".format(addr, port))

    def run(self, max_connection=1):
        self.listen(max_connection)

        # 与客户端成功建立连接后，返回一个元组(client_socket,address_information)
        # 其中，address_information是一个元组(address,port)
        cli_sock, cli_addr = self.socket.accept()
        print("[+] Accepted connection from: {}：{:d}".format(*cli_addr))

        self.handle_client(cli_sock)

    def print_sessions(self):
        for session in self.sessions:
            session.print_data()

# server=TCPServer()
# server.run()