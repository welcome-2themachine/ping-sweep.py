#! /usr/bin/python3

# File: ping_sweep.py
# Project: Net_Map
# Created Date: Fri, 30 July 2021 @ 2159
# Author: welcome-2themachine

import threading
from ps_functions import *
# install dependencies - eventually this will be a requirements.txt


"""
TO DO:
    - map the network for hosts that respond to ping
    - modify get functions to take interface name as a parameter, or default if no parameter
    - multithread pings (divide range into equal parts and append once sweep is done)
    - add wait time speficication
"""

up = []


interface = pick_interface()
print(interface)
netinf = getnetworkinfo(interface)

up_lock = threading.Lock()
print(netinf)

# this function is a "to do" for multithreading - more to follow
def thread_task(ip_list):
    for i in ip_list:
        if myping(i)==0:
            up.append(i)

targets=buildtargetrange(netinf)
print(targets)

"""
for host in scanrange:
    if myping(hostname, platform) == 0:
        up.append(host)
print(up)
"""
