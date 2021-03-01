from TCP_client_Class import TCPClient
import sys
import getopt


# RHOST='127.0.0.1'
# RPORT=6666
# FILE_NAME='test.txt'


# 获取参数
opts, args = getopt.getopt(sys.argv[1:], 'h:p:f:')
params = dict(opts)

if not params.get('-h', False) and not params.get('-p', False) and not params.get('f', False):
	print('USAGE: python3 Client.py -h RHOST -p RPORT -f FILE')
	exit()

RHOST = params['-h']
RPORT = int(params['-p'])	#记得转换成int
FILE_NAME = params['-f']

client = TCPClient(RHOST, RPORT)
client.connect()

with open(FILE_NAME, 'rb') as fileobj:
	print('[*] Sending {}'.format(FILE_NAME))
	# 首先发送文件名
	client.send(FILE_NAME.encode('utf-8'))
	# 再发送文件本体
	client.send(fileobj.read())

client.close()
