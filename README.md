**To Run ping_sweep.py:**
    `python3 ping_sweep.py`

**What it does:**

    - automatically detects your default network
    
    - detects network size, and total number of IPs in the network

    - sends one ping to each ip in the address space

**Roadmap:**

    - implement runtime args:
        help
        interface selection
        ping wait times
        ip scan range
    - multithread (to increase performace)
    - allow interface selection
    - make it pretty

**Dependencies (as of 1AUG21):**

    - python3
    - python libraries: os, ipaddress, platform, threading, netifaces
