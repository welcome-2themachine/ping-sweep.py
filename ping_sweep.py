#! /usr/bin/python3

# File: ping_sweep.py
# Project: Net_Map
# Created Date: Fri, 30 July 2021 @ 2159
# Author: welcome-2themachine

import os, ipaddress, platform, threading
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
def myping(hostname):
    if getplatform()=='linux':
        response = os.system("ping -c 1 -w 2 " + hostname)
    elif getplatform()=='windows':
        response = os.system("ping -n 1 -w 2" + hostname)
    return response

# function returns host ip, netmask, and gateway
def getnetworkinfo(interface):
    info = {'ip': "0.0.0.0", 'netmask': "0.0.0.0", 'network': "0.0.0.0", 'broadcast': "0.0.0.0", 'gateway': "0.0.0.0", '/': "0"}
    info['ip']=gethostip(interface)
    info['netmask']=getnetmask(interface)
    info['network']=getnetworkip(interface)
    info['broadcast']=getbroadcast(interface)
    info['gateway']=getgateway(interface)
    info['/']=getslash(interface)
    return info

# function that gets the host ip
def gethostip(interface):
    hostip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
    return hostip

# function that gets the netmask
def getnetmask(interface):
    netmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
    return netmask

# function that gets the network ip
def getnetworkip(interface):
    network_ip_list=["0","0","0","0"]
    ip = gethostip(interface)
    netmask = getnetmask(interface)

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
def getbroadcast(interface):
    broadcast = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['broadcast']
    return broadcast

# function that gets the default gateway ip - no gateway is 0.0.0.0
def getgateway(interface):
    try:
        gateway = netifaces.gateways()[interface][netifaces.AF_INET][0]
    except:
        gateway = "0.0.0.0"
    return gateway

# funtion that determines the slash size of the network (192.168.0.1/24)
def getslash(interface):
    slash = 32
    netmask = getnetmask(interface)
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

def getplatform():
    return platform.system().lower()

def thread_task(ip_list):
    for i in ip_list:
        if myping(i)==0:
            up.append(i)

def printmenu():
    print("Select interface to scan (ENTER for default): ")
    for i in range(len(netifaces.interfaces())):
        if getdefaultinterface() == netifaces.interfaces()[i]:
            print(str(i) + ") "+netifaces.interfaces()[i]+" *default*")
        else:
            print(str(i) + ") " + netifaces.interfaces()[i])

def testuserinput(input):
    if input.isdigit(): 
        if 0 <= int(input) < len(netifaces.interfaces()):
            return True
    elif input in netifaces.interfaces():
        return True
    else:
        return False

def pick_interface():
    #testing the user's input
    good_input=False
    selection=""
    while good_input is False:
        printmenu()
        selection = input(": ")
        if testuserinput(selection):
            good_input = True
        else:
            print("Please select an interface using the name or number of the interface")
    if selection.isdigit():
        return netifaces.interfaces()[int(selection)]
    elif selection in netifaces.interfaces():
        return selection
    elif selection == "": 
        return getdefaultinterface()
    else:
        return selection

interface = pick_interface()
print(interface)
netinf = getnetworkinfo(interface)

up_lock = threading.Lock()
scanrange = []

for host in ipaddress.IPv4Network(netinf['network']+'/'+netinf['/']):
    scanrange.append(str(host))

"""
for host in scanrange:
    if myping(hostname, platform) == 0:
        up.append(host)
print(up)
"""
