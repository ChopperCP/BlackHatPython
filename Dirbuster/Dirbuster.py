import queue
import requests
import threading
import sys
import getopt
import time



# UI
def usage():
	print('USAGE: python3 Dirbuster.py -f <wordlist> -u <URL> [-t threads=10]')
	print('\t-h: display this help message')


opts, args = getopt.getopt(sys.argv[1:], "f:u:t:")
opts = dict(opts)
WORDLIST = ''
THREADS = 10
URL = ''

if '-h' in opts or len(opts.keys()) == 0 or '-f' not in opts or '-u' not in opts:
	usage()
	quit()
if '-f' in opts:
	WORDLIST = opts['-f']
if '-u' in opts:
	URL = opts['-u']
if '-t' in opts:
	THREADS = int(opts['-t'])

# 准备目录序列
directories = queue.Queue()
with open(WORDLIST, 'r') as fileobj:
	#一定要记得去掉右边的\n
	line = fileobj.readline().rstrip('\n')
	while len(line) != 0:
		directories.put(line)
		#一定要记得去掉右边的\n
		line = fileobj.readline().rstrip('\n')

# 定义访问函数
def dirbust(delay=0,retry=3):
	global directories

	while not directories.empty():
		directory = directories.get()
		# 使用HTTP请求
		response = requests.get('http://' + URL + directory)
		# 响应值为200时回显
		if response.status_code == 200:
			print('[200] http://{}{}'.format(URL, directory))
		else:
			#重试retry次
			for _ in range(0,retry):
				response = requests.get('http://' + URL + directory)
				# 响应值为200时回显
				if response.status_code == 200:
					print('[200] http://{}{}'.format(URL, directory))
					break
				time.sleep(delay)
		time.sleep(delay)


for _ in range(0, THREADS):
	thread = threading.Thread(target=dirbust)
	thread.start()
