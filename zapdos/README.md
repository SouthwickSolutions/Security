## zapdos.sh

#### V. 20170109

This script performs various hiding  and spoofing techniques. Some listed tasks are redundant. This script was a personal exercise mixing bash scripting and security. Kali is the ideal OS for this script. This script does the following in this order:
1. collects info on all the different interfaces (up to 10)
2. changes the name of the connected interface to a random string
3. changes the hostname to a random string
4. turns off IPv6 for all interfaces
5. spoof MAC address for all interfaces
6. turns on anonsurf
7. adds more DNS servers to what anonsurf has provided


***Script must be run as root***