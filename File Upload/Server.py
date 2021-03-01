from TCP_Server_Class_v3 import *
import getopt
import sys

# LHOST='127.0.0.1'
# LPORT=6666

# 获取参数
opts, args = getopt.getopt(sys.argv[1:], 'h:p:')
params = dict(opts)

if not params.get('-h', False) and not params.get('-p', False):
	print('USAGE: python3 Server.py -h LHOST -p LPORT')
	exit()

LHOST = params['-h']
LPORT = int(params['-p'])	#记得转换成int


server=TCPServer(LHOST,LPORT)
server.run()