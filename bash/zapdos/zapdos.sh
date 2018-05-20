#!/bin/bash
<<purpose
   This script does the following in this order-
       1.) collects info on all the different interfaces (up to 10)
       2.) changes the name of the connected interface to a random string
       3.) changes the hostname to a random string
       4.) turns off IPv6 for all interfaces
       5.) spoof MAC address for all interfaces
       6.) turns on anonsurf
       7.) adds more DNS servers to what anonsurf has provided

       ***Script must be run as root***

       Programs/Packages Needed
       ------------------------
       anonsurf

       Potential Future Features
       -------------------------
       change UUID of interfaces and things
       
       DNS Resources
       -------------
       see https://api.opennicproject.org/geoip/?help for arguments

       List of variables in order of appearance
       ----------------------------------------
       filepath:           path of where log is housed
       now:                current date and time
       interface_list:     list of current interfaces
       interface_count:    number of interfaces from interface_list
       new_interface_name: randomly generated interface name
       random_length:      randomly generated number between 5-10
       new_hostname:       randomly generated hostname
       c2:                 column 2
       dns_list:           (temporary file) stores 3 dozenish randomly selected DNS servers
       random_dns:         stores 10 randomly selected DNS servers from dns_list
       IFS:                internal field seperator used to help read resolv.conf
purpose

filepath='/root/Desktop/zapdos.log'

#creates log file
echo "ZAPDOS LOG" > $filepath
echo "----------" >> $filepath
now=$(date)
echo $now >> $filepath
echo >> $filepath
echo >> $filepath

#1.) collect the different interfaces
#stores each interface
interface_list=$(netstat -i|awk '{print $1}'|sed -n '3,9p;10q')
echo "    List of interfaces:" >> $filepath
echo "    -------------------" >> $filepath
echo "    "$interface_list >> $filepath
now=$(date +%T)
echo >> $filepath
echo $now >> $filepath

interface_count=$(echo $interface_list|grep -o " "|wc -l)
interface_count=$(($interface_count+1))
echo >> $filepath
echo "    Number of interfaces (including loopback):" $interface_count >> $filepath
now=$(date +%T)
echo >> $filepath
echo $now >> $filepath
echo >> $filepath

#2.) change the names of the connected interfaces
for i in $interface_list; do
	echo -n "    Interface" $i >> $filepath
	new_interface_name=$(pwgen 4 1)
	ifconfig $i down
	ip link set $i name $new_interface_name
	ifconfig $new_interface_name up
	echo " changed to:" $new_interface_name >> $filepath
done

echo >> $filepath
now=$(date +%T)
echo $now >> $filepath
echo >> $filepath

#shuts down interfaces to be worked on
nmcli r all off
nmcli r all on

sleep 10

#stores the new interface names
interface_list=$(netstat -i|awk '{print $1}'|sed -n '3,9p;10q')
echo "    List of new interfaces:" >> $filepath
echo "    -----------------------" >> $filepath
echo "    "$interface_list >> $filepath
now=$(date +%T)
echo >> $filepath
echo $now >> $filepath
echo >> $filepath

#3.) change the hostname
random_length=$(shuf -i 5-10 -n 1)
new_hostname=$(pwgen $random_length 1)
echo "    Current hostname:" $HOSTNAME >> $filepath
hostname $new_hostname
echo "    Hostname changed to:" $new_hostname >> $filepath
echo >> $filepath
now=$(date +%T)
echo $now >> $filepath
echo >> $filepath

#4.) turns off IPv6 for all interfaces
echo -n "    Your current IPv6 address is: " >> $filepath
echo $(ip addr show | sed -e's/^.*inet6 \([^ ]*\)\/.*$/\1/;t;d') >> $filepath
echo >> $filepath
echo "    ***If a value is listed, anonsurf will turn this off" >> $filepath
echo "    If a value is not listed, there is no IPv6 address***" >> $filepath
echo >> $filepath
now=$(date +%T)
echo $now >> $filepath
echo >> $filepath

#5.) spoof mac address for all interfaces
#retrieves and lists current MAC address for each interface
echo "    Current MAC addresses for interfaces:" >> $filepath
echo "    -------------------------------------" >> $filepath
for i in $interface_list;do
	echo -n "   " $i": " >> $filepath 
	echo $(ifconfig $i | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}') >> $filepath
done

echo >> $filepath
echo "    ***If no MAC address is listed, interface has none***" >> $filepath
echo >> $filepath

#changes and lists the new MAC addresses for each interface
for i in $interface_list;do
        ifconfig $i hw ether 00:24:A8:C6:FC:24
done
echo "    New MAC addresses for interfaces:" >> $filepath
echo "    ---------------------------------" >> $filepath
for i in $interface_list;do
	echo -n "   " $i": " >> $filepath
	echo $(ifconfig $i | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}') >> $filepath
done

echo >> $filepath
now=$(date +%T)
echo $now >> $filepath
echo >> $filepath

#6.) turns on anonsurf
#check public ip address before anonsurf
echo -n "    Public IP address before anonsurf turned on: " >> $filepath
curl ipinfo.io/ip >> $filepath
echo >> $filepath
now=$(date +%T)
echo $now >> $filepath

anonsurf start > /dev/null

echo >> $filepath
echo "    Anonsurf turned on" >> $filepath
echo >> $filepath
now=$(date +%T)
echo $now >> $filepath
echo >> $filepath

#check public ip address after anonsurf
echo -n "    Public IP address after anonsurf turned on: " >> $filepath
curl ipinfo.io/ip >> $filepath
echo >> $filepath
now=$(date +%T)
echo $now >> $filepath
echo >> $filepath

#7.) adds more DNS servers to what anonsurf has provided
#lists current dns servers
echo "    Current name servers:" >> $filepath
echo "    ---------------------" >> $filepath
nmcli dev show | grep DNS | while read c1 c2; do echo "   " $c2 >> $filepath ; done
echo >> $filepath
now=$(date +%T)
echo $now >> $filepath
echo >> $filepath

#adds and list new nameservers
wget 'https://api.opennicproject.org/geoip/?res=30&adm=15&bare&rnd=true' -O- >> dns_list
random_dns=$(shuf -n 10 dns_list)
for i in $random_dns; do
	echo "nameserver" $i >> /etc/resolv.conf
done
rm dns_list

echo "    Name servers changed to:" >> $filepath
echo "    ------------------------" >> $filepath
IFS=$'\n'
for i in $(cat /etc/resolv.conf); do
	echo "    "$i >> $filepath
done

echo >> $filepath
now=$(date +%T)
echo $now >> $filepath
echo >> $filepath
