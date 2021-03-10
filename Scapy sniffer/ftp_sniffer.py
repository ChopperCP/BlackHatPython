from scapy.all import *


def process_packet(packet):
	payload = bytes(packet[TCP].payload)
	payload = payload.decode()
	print(payload)


# FTP works on port 20 and 21
sniff(prn=process_packet, filter="port 20 or port 21")
