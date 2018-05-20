#/bin/bash

#update system
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get autoremove -y #uninstalls packages that are no longer needed
sudo apt-get autoclean
sudo apt-get clean #removes installers that are not needed

#update nessus
/opt/nessus/sbin/nessuscli update
