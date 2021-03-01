import subprocess
from TCP_Client_Classv2 import TCPClient
from TCPServer_Simple import *
import sys
import getopt


def open_shell(session:Session):
	def exac(cmd:str):
		'''执行cmd并返回结果'''
		output=subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
		return output

	while True:
		try:
			cmd=session.receive().decode('utf8')
			session.send(exac(cmd))
		except:
			session.send('Command not found or execution error.'.encode('gbk'))

def get_shell(client:TCPClient):
	def print_n_receive():
		while True:
			# print(client.receive().decode('utf8'))	#linux
			print(client.receive().decode('gbk'))		#windows

	receive_handler=threading.Thread(target=print_n_receive)
	receive_handler.setDaemon(True)
	receive_handler.start()

	while True:
		try:
			cmd=input('shell>')+'\n'
			client.send(cmd.encode('utf8'))
		except KeyboardInterrupt:
			client.close()

def usage():
	print('USAGE: ')
	print('\tServer: -s <local IP> <listen port>')
	print('\tClient: -c <remote IP> <remote port>')
	print('\t-h: Display this help message')

class Host(TCPServer):
    def handle_client(self, client_socket: socket):
        '''开始接受并处理数据'''
        addr, port = client_socket.getsockname()

        # 处理函数
        session=Session(client_socket)
        open_shell(session)

        session.close()
        print("[-] Connection {}:{} closed".format(addr, port))



opts,args=getopt.getopt(sys.argv[1:],"sch")
opts=dict(opts)
IP='127.0.0.1'
port=6666

if ('-s' in opts and '-c' in opts) or '-h' in opts or len(args)!=2:
	usage()
	quit()

elif '-s' in opts:
	IP=args[0]
	port=int(args[1])

	host=Host(IP,port)
	host.run()

elif '-c' in opts:
	IP=args[0]
	port=int(args[1])

	client=TCPClient(IP,port)
	client.connect()
	get_shell(client)






