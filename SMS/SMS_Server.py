from TCP_Server_Class_v3 import *
import threading
import time
import getopt
import sys


# 获取参数
opts, args = getopt.getopt(sys.argv[1:], 'h:p:')
params = dict(opts)

if not params.get('-h', False) and not params.get('-p', False) and not params.get('f', False):
	print('USAGE: python3 SMS_Server.py -h LHOST -p LPORT')
	exit()

LHOST = params['-h']
LPORT = int(params['-p'])	#记得转换成int




# def send(session:Session):
# 	while True:
# 		msg=input('>')
# 		session.send(msg.encode('utf-8'))

# def receive(session:Session):
# 	while True:
# 		try :
# 			session.receive()
# 		except:
# 			pass



server=TCPServer(LHOST,LPORT)
try:
	server.run()
except:
	exit()
#仅支持一个session，仍有扩展空间

# for session in server.sessions:
# 	send_handler=threading.Thread(target=send,args=(session,))
# 	send_handler.setDaemon(True)
# 	send_handler.start()

# 	recv_handler=threading.Thread(target=receive,args=(session,))
# 	recv_handler.setDaemon(True)
# 	recv_handler.start()

# try:
# 	#保持主进程活跃不退出
# 	time.sleep(10000)
# except KeyboardInterrupt:
# 	exit()