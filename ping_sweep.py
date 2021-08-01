#! /usr/bin/python3

# File: ping_sweep.py
# Project: Net_Map
# Created Date: Fri, 30 July 2021 @ 2159
# Author: welcome-2themachine

import os, ipaddress, platform
# install dependencies - eventually this will be a requirements.txt
try:
    import netifaces
except:
    import pip
    pip.main(['install', '-U', 'netifaces'])

"""
TO DO:
    - map the network for hosts that respond to ping
    - modify get functions to take interface name as a parameter, or default if no parameter
    - multithread pings (divide range into equal parts and append once sweep is done)
    - add wait time speficication
"""

up = []

# function to send one ICMP ping to a given hostname
def myping(hostname, platform):
    if platform.lower()=='linux':
        response = os.system("ping -c 1 -w 2 " + hostname)
    elif platform.lower()=='windows':
        response = os.system("ping -n 1 -w 2" + hostname)
    return response

# function returns host ip, netmask, and gateway
def getnetworkinfo():
    info = {'ip': "0.0.0.0", 'netmask': "0.0.0.0", 'network': "0.0.0.0", 'broadcast': "0.0.0.0", 'gateway': "0.0.0.0", '/': "0"}
    info['ip']=gethostip()
    info['netmask']=getnetmask()
    info['network']=getnetworkip()
    info['broadcast']=getbroadcast()
    info['gateway']=getgateway()
    info['/']=getslash()
    return info

# function that gets the host ip
def gethostip():
    hostip = netifaces.ifaddresses(getdefaultinterface())[netifaces.AF_INET][0]['addr']
    return hostip

# function that gets the netmask
def getnetmask():
    netmask = netifaces.ifaddresses(getdefaultinterface())[netifaces.AF_INET][0]['netmask']
    return netmask

# function that gets the network ip
def getnetworkip():
    network_ip_list=["0","0","0","0"]
    ip = gethostip()
    netmask = getnetmask()

    ip_list = ip.split(".")
    netmask_list = netmask.split(".")

    for i in range(len(netmask.split("."))):
        if int(netmask.split(".")[i])==255:
            network_ip_list[i]=ip.split(".")[i]
        else:
            network_ip_list[i]=str(int(ip.split(".")[i]) & int(netmask.split(".")[i]))
            break
    network_ip = ".".join(network_ip_list)
    return network_ip

# function that finds the default network interface
def getdefaultinterface():
    iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    return iface

# function that gets the broadcase address
def getbroadcast():
    broadcast = netifaces.ifaddresses(getdefaultinterface())[netifaces.AF_INET][0]['broadcast']
    return broadcast

# function that gets the default gateway ip
def getgateway():
    gateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
    return gateway

# funtion that determines the slash size of the network (192.168.0.1/24)
def getslash():
    slash = 32
    netmask = getnetmask()
    for i in netmask.split("."):
        if i == "0":
            break
        elif i == "255":
            slash -= 4
        else:
            shift = int(i) ^ 255
            while shift > 0:
                slash -= 1
                shift = shift >> 1
            break
    return str(slash)

netinf = getnetworkinfo()
platform = platform.system()
scanrange = []
for host in ipaddress.IPv4Network(netinf['network']+'/'+netinf['/']):
    scanrange.append(str(host))

"""
for host in scanrange:
    if myping(hostname, platform) == 0:
        up.append(host)
print(up)
"""
