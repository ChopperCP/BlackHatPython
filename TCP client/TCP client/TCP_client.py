import os
import socket

target_host = "127.0.0.1"      #目标主机
target_port = 9999				#目标端口

# 1.建立Socket
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# 2.建立TCP连接
client.connect((target_host,target_port))
# 3.发送数据
client.send(b"Gimme some data")
# 4.接收数据
response = client.recv(8192)        #保存数据的缓存区的大小（字节数）
print(response)
# 5.关闭连接
client.close()
