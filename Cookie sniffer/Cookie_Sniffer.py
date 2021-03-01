from scapy.all import *


def get_tcp_payload(packet: Packet):
	if packet[TCP].payload:
		cookie_packet=bytes(packet[TCP].payload).split(b'\n')
		for line in cookie_packet:
			if b'Cookie' in line or b'GET /' in line:
				print(line)
	print('\n')



sniff(filter='tcp port 80', iface='Killer(R) Wireless-AC 1550i Wireless Network Adapter (9560NGW)',
      prn=get_tcp_payload, store=False)
