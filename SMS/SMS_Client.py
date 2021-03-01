from TCP_Client_Class import TCPClient
import threading
import time
import getopt
import sys


# 获取参数
opts, args = getopt.getopt(sys.argv[1:], 'h:p:')
params = dict(opts)

if not params.get('-h', False) and not params.get('-p', False) and not params.get('f', False):
	print('USAGE: python3 SMS_Client.py -h RHOST -p RPORT')
	exit()

RHOST = params['-h']
RPORT = int(params['-p'])	#记得转换成int




client=TCPClient(RHOST,RPORT)
try:
	client.connect()
except:
	print('[!] Connection to {}:{} failed'.format(RHOST,RPORT))
	exit()

def send(client:TCPClient):
	while True:
		msg=input('>')
		client.send(msg.encode('utf-8'))

def receive(client:TCPClient):
	while True:
		try :
			client.receive()
		except:
			pass



send_handler=threading.Thread(target=send,args=(client,))
send_handler.setDaemon(True)
send_handler.start()

recv_handler=threading.Thread(target=receive,args=(client,))
recv_handler.setDaemon(True)
recv_handler.start()

try:
	#保持主进程活跃不退出
	time.sleep(10000)
except KeyboardInterrupt:
	exit()