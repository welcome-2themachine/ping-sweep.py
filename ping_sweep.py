#! /usr/bin/python3

# File: ping_sweep.py
# Project: Net_Map
# Created Date: Fri, 30 July 2021 @ 2159 HST
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
    - add wait time speficication
"""
# setup the argument parsing
args=setup_parser().parse_args()
"""
    To get to the parsed arguments: grab args.interface, args.wait (they will be the defaults unless the user changes them)
"""
print_welcome()
up = []
if args.interface == "empty":
    interface = pick_interface()
else:
    interface = args.interface
wait = args.wait
netinf = getnetworkinfo(interface)
targets = buildtargetrange(netinf)
print(interface)
print(netinf)

up_lock = threading.Lock()

# this function is a "to do" for multithreading - more to follow
def thread_task(ip_list):
    for i in ip_list:
        if myping(i, wait)==0:
            up.append(i)

"""
for host in scanrange:
    if myping(hostname, platform) == 0:
        up.append(host)
print(up)
"""