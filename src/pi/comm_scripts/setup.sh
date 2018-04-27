#!/bin/sh
# This script sets up '/etc/network/interfaces' and '/etc/rc.local' so that
# the Raspberry Pi always begins by trying to create and join a mesh ad-hoc
# network called 'bakery'.
if [ $# == 1 ]
then
    if [ -e "/etc/network/interfaces" ] && [ ! -e "/etc/network/interfaces.commsav" ]
    then
        sudo mv "/etc/network/interfaces" "/etc/network/interfaces.commsav"
        sudo printf "Saving /etc/network/interfaces as /etc/network/interfaces.commsav\n"
    fi
    sudo touch "/etc/network/interfaces"
    sudo printf "allow-hotplug wlan0\nauto wlan0\niface wlan0 inet static\n\taddress $1\n\tnetmask 255.255.255.0\n\tgateway 192.168.1.1\n" >> "/etc/network/interfaces"
    if [ -e "/etc/rc.local" ] && [ ! -e "/etc/network/rc.local.commsav" ]
    then
        sudo mv "/etc/rc.local" "/etc/rc.local.commsav"
        sudo printf "Saving /etc/rc.local as /etc/rc.local.commsav\n"
    fi
    sudo touch "/etc/rc.local"
    sudo printf "#!/bin/sh\niwconfig wlan0 mode ad-hoc channel 11 essid \"bakery\"\n\nexit 0" >> "/etc/rc.local"
    sudo chmod +x /etc/rc.local
else
    echo "You must supply exactly 1 argument, the IP address of this device (ex: 192.168.1.2)"
fi