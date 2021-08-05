#! /usr/bin/python3

# File: ping_sweep.py
# Project: Net_Map
# Created Date: Tue, 3 Aug 2021 @ 2223
# Author: welcome-2themachine

import os, platform, ipaddress

try:
    import netifaces
except:
    import pip
    pip.main(['install', '-U', 'netifaces'])
    

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
    try: broadcast = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['broadcast']
    except: broadcast = "255.255.255.255"
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
            slash += 4
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

#ensures the correct ping command is used by detecting the type of OS being run
def getplatform():
    return platform.system().lower()

# prints the menu the user selects the interface from
def printmenu():
    print("Select interface to scan (ENTER for default): ")
    for i in range(len(netifaces.interfaces())):
        if getdefaultinterface() == netifaces.interfaces()[i]:
            print(str(i) + ") "+netifaces.interfaces()[i]+" *default*")
        else:
            print(str(i) + ") " + netifaces.interfaces()[i])

# ensures the user picks a valid interface
def testuserinput(input):
    if input.isdigit(): 
        if 0 <= int(input) < len(netifaces.interfaces()):
            return True
    elif input in netifaces.interfaces():
        return True
    else:
        return False

# allows user to select interface with number key or interface name
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

# builds the target range to scan
def buildtargetrange(netinf):
    scanrange=[]
    for host in ipaddress.IPv4Network(netinf['network']+'/'+netinf['/']):
        scanrange.append(str(host))
    return scanrange