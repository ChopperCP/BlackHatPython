import socket
import threading
import os

# #处理数据
# def handle_client(client_socket):
# 	addr,port = client_socket.getsockname()

# 	request=client_socket.recv(1024)

# 	print("[*] Recieved: {} \t from {}:{}".format(str(request),addr,port))

# 	client_socket.send(b"This is ChopperCP's TCP server. This is the only pack you will recieve.")

# 	client_socket.close()

# 	print("[-] Connection {}:{} closed".format(addr,port))





# bind_ip='0.0.0.0'   #监听所有ip
# bind_port=9999      #监听端口 

# # 创建套接字
# server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# # 绑定端口和IP
# server.bind((bind_ip,bind_port))
# #最大连接数
# server.listen(5)

# print("[*] Listening on "+bind_ip+':'+str(bind_port))


# #主循环，接收和发送数据
# while True:
# 	#与客户端成功建立连接后，返回一个元组(client_socket,address_information)
# 	#其中，address_information是一个元组(address,port)
#     client,addr =server.accept()

#     print ("[+] Accepted connetion form: {}：{:d}".format(*addr))
#     #挂起线程，处理数据
#     client_handler=threading.Thread(target=handle_client,args=(client,))    #args是一个只有一个元素的元组，传入target函数的参数
#     client_handler.start()

class TCPServer():
	def __init__(self,bind_ip='0.0.0.0',port=9999):
		# 创建套接字
		self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.addr=(bind_ip,port)
		# 绑定端口和IP
		self.socket.bind(self.addr)
		self.data=[]	#所有接受的数据

	def listen(self,max_connetion=5):
		'''开始监听'''
		self.socket.listen(max_connetion)
		print("[*] Listening on {}:{}".format(*self.addr))

	def handle_client(self,client_socket:socket,data:bytes,buffer=1024):
		'''开始接受并处理数据'''
		addr,port = client_socket.getsockname()
		# 接收数据
		request=client_socket.recv(buffer)
		self.data.append(request.decode('utf-8'))
		# print("[*] Recieved: {} \t from {}:{}".format(str(request),addr,port))
		# 发送数据
		client_socket.send(data)
		client_socket.close()
		print("[-] Connection {}:{} closed".format(addr,port))

	def run(self,data:bytes,max_connection=5,buffer=1024):
		self.listen(max_connection)
		#主循环，接收和发送数据
		while True:
			#与客户端成功建立连接后，返回一个元组(client_socket,address_information)
			#其中，address_information是一个元组(address,port)
		    cli_sock,cli_addr =self.socket.accept()

		    print ("[+] Accepted connetion form: {}：{:d}".format(*cli_addr))
		    #挂起线程，处理数据
		    cli_handler=threading.Thread(target=self.handle_client,args=(cli_sock,data,buffer))    #args是一个只有一个元素的元组，传入target函数的参数
		    cli_handler.start()

	def print_data(self):
		print('\tConnetion {}:{} has received:'.format(*self.addr))
		line_no=1
		for line in self.data:
			#行号居左，宽度为4
			print('\t{:<4}| {}'.format(line_no,line))
			line_no+=1



server=TCPServer()
server.run(data=b'This is a TCP server.')
server.print_data()
os.system('pause')

