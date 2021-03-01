import socket

socket.setdefaulttimeout(10)        #超时的时间（s）

target_host = "8.8.8.8"             #目标服务器
target_port = 80                    #目标端口

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto("ping".encode('utf-8','strict'),(target_host,target_port))

response = client.recvfrom(4096)

print(response)



