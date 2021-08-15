**To Run ping_sweep.py:**
    standard example: `python3 ping_sweep.py`
    example with options `python3 ping_sweep.py --interface wlan0 --wait 5`
    -- interface: select the interface
    -- wait: selects the wait time for a ping response
    get help: `python3 ping_sweep.py -h` or `python3 ping_sweep.py --help`

**What it does:**

    - automatically detects your default network
<<<<<<< HEAD
    
    - allows you to select interface
    
=======
>>>>>>> release
    - detects network size, and total number of IPs in the network
    - sends one ping to each ip in the address space
    - new features
        - allows the user to select interface
        - displays the correct network name on windows systems
        - cool ascii art
        - a help menu
        - command line args to select interfaces and adjust wait time

**Roadmap:**

    - implement runtime args:
<<<<<<< HEAD
        help
        ping wait times
=======
>>>>>>> dev
        ip scan range
    - multithread (to increase performace)
    - make it pretty

**Dependencies (as of 14AUG21):**

    - python3
    - python libraries: os, ipaddress, platform, threading, netifaces, winreg
