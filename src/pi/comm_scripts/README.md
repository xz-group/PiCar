This project contains the programs used to communicate between Pi Cars. This was completed
as an ESE 205 project at Washington University in St. Louis in the Spring 2018 semester in
conjunction with Dr. Xuan 'Silvia' Zhang. The project leverages the Pi Car platform to 
enable vehicluar ad hoc communication designed to allow for scaled testing.

Students:
Patrick Naughton
Yak Fishman
Jacob Cytron

TA:
Sam Hoff

Instructor:
Dennis Mell

<h1>Setup</h1>
To use this project, first clone the repository into the directory of your project (https://github.com/patricknaughton01/comm_scripts.git).
Run
`sudo bash ./setup.sh 192.168.1.xxx`
(where xxx is a unique 8 bit identifier for the car, such as `3` or `17` or `250`) from the terminal (within the `comm_scripts` directory) to set up the mesh network. This will disable normal networking but will save the two files it modifies. These two files are
`/etc/network/interfaces` which is saved as `/etc/network/interfaces.commsav`
`/etc/rc.local` which is saved as `/etc/rc.local.commsav`
Example
`sudo bash ./setup.sh 192.168.1.7`
will setup the Pi to join a mesh network on startup and set its static IP address to 192.168.1.7.

<h1>Import</h1>
Within your project, for any script that needs networking, simply type
`from core.network import Network`
to gain access to the network class. Then `network = Network(1024, 10)` will setup a new `Network` object that can read in 1024 byte packets and stores the last 10 messages it received before refusing to read in any more.
