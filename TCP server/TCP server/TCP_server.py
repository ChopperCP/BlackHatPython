import socket
import threading

# 处理数据


def handle_client(client_socket):
    addr, port = client_socket.getsockname()

    request = client_socket.recv(1024)

    print("[*] Recieved: {} \t from {}:{}".format(str(request), addr, port))

    client_socket.send(
        b"This is ChopperCP's TCP server. This is the only pack you will recieve.")

    client_socket.close()

    print("[-] Connection {}:{} closed".format(addr, port))


bind_ip = '0.0.0.0'  # 监听所有ip
bind_port = 9999  # 监听端口

# 创建套接字
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定端口和IP
server.bind((bind_ip, bind_port))
# 最大连接数
server.listen(5)

print("[*] Listening on " + bind_ip + ':' + str(bind_port))


# 主循环，接收和发送数据
while True:
    # 与客户端成功建立连接后，返回一个元组(client_socket,address_information)
    # 其中，address_information是一个元组(address,port)
    client, addr = server.accept()

    print("[+] Accepted connetion form: {}：{:d}".format(*addr))
    # 挂起线程，处理数据
    client_handler = threading.Thread(target=handle_client, args=(
        client,))  # args是一个只有一个元素的元组，传入target函数的参数
    client_handler.start()
