#! /usr/bin/python3

# File: ping_sweep.py
# Project: Net_Map
# Created Date: Fri, 30 July 2021 @ 2159 EST
# Author: welcome-2themachine

"""
TO DO:
    - map the network for hosts that respond to ping
    - multithread pings (divide range into equal parts and append once sweep is done)
"""

import concurrent.futures
from ps_functions import *

# setup the argument parsing
"""
    To get to the parsed arguments: grab args.interface, args.wait (they will be the defaults unless the user changes them)
"""
args=setup_parser().parse_args()
# print the welcome message
print_welcome()
# check for user args
if args.interface == "empty":
    interface = pick_interface()
else:
    interface = args.interface
wait = args.wait
netinf = getnetworkinfo(interface)
targets = buildtargetrange(netinf)
# setup thread pool
up = []
print(targets)
print(netinf)
def worker(host_ip):
    response = myping(host_ip, wait, interface)
    if response == 0:
        up.append(host_ip)

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for host in targets:
        futures.append(executor.submit(worker, host_ip=host))
print(up)
