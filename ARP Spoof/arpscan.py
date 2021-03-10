from scapy.all import *


def arpscan(CIDR):
	requests = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=CIDR)  # make ARP requests
	responses, unanswered = srp(requests, timeout=5, verbose=1)  # send requests, listen for 5s
	for response in responses:
		send, recv = response
		print("[*]{} at {} is alive.".format(recv[ARP].psrc, recv[ARP].hwsrc))


arpscan("172.26.104.0/24")
