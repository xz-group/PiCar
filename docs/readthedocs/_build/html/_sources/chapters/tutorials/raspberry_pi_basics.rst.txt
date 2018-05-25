Raspberry Pi Basics
=======================

A small crash course on setting up and using the Raspberry Pi
(as a server, ftp storage, home-base, etc.)

What is a Raspberry Pi?
-----------------------
A `Raspberry Pi <https://www.raspberrypi.org/>`_ is a credit card sized
computer that can run Linux (and other OS) to do almost anything your computer
can do. It can be simply connected to a monitor/TV, keyboard and mouse and
be used as a regular computer. Because of its low power consumption, it is
used as a web-server, file storage system, home automation system, etc. It
can also be connected to an Arduino to aid in robotics such as the PiCar.

Setting up a Raspberry Pi with SSH
----------------------------------
Materials Required
^^^^^^^^^^^^^^^^^^
- Raspberry Pi 3 B+ (older models will also work)
- Pi compatible power adapter
- Micro SD Card (with alteast 16GB of memory; you may need an SD card adapter
  to connect it to your computer)
- USB keyboard and mouse
- Access to a monitor + HDMI cable
- Access to your router, or a new router
- A laptop for remote access to the Pi

Procedure
^^^^^^^^^
.. note:: If you are a Washington University student working on the PiCar
          project, you can skip to step 10 and use the given IP address of
          the Pi to communicate with the Pi. However it is recommended to
          atleast glance through the steps to see what was done.

1. Download the `Raspbian Stretch with Desktop
   <https://www.raspberrypi.org/downloads/raspbian/>`_ image.
2. Download `Etcher <https://etcher.io/>`_
3. Install Raspbian OS to the Raspberry Pi:

   * Insert SD card into your computer.
   * Run `Etcher`.
   * In `Etcher`, choose the downloaded Raspbian zip or image file.
   * Choose the SD Card drive

     .. warning:: Ensure to select the correct drive (SD Card) because it will
                  be formatted.
   * Flash the Raspbian image.
   * Eject SD card and put it into the Raspberry Pi.

4. Connect the mouse, keyboard and monitor to the Raspberry Pi. Finally
   connect the power cable to turn on the Raspberry Pi.

5. The default login credentials for the Raspberry Pi are:

   * username: ``pi``
   * password: ``raspberry``

6. Change the password to your liking by opening the terminal and typing:

   .. code-block:: bash

     sudo passwd pi

7. Use the following command to enable SSH (Secure Shell) which will be used
   to communicate to your computer wirelessly.

   .. code-block:: bash

     sudo raspi-config

   * Navigate to ``Interfacing Options`` >> ``SSH`` >> ``Enable``

8. Connect the Pi to your router (which is connected to your company/university
   internet port) and reboot the Pi using:

   .. code-block:: bash

     sudo reboot now

9. Get the local IP address of your Pi using:

   .. code-block:: bash

     hostname -I

   * You will find your Pi's local IP (eg: `192.168.1.123`)
   * Alternatively you can navigate to the router admin page to check the
     IP addresses of connected devices.

10. On your laptop, connect to the router and use the following instructions
    based on your OS:

    Windows:
     * Download `Putty
       <https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html>`_
     * Run `Putty`
     * For the hostname, use the IP address you got for the Pi (eg:
       ``pi@192.168.123``), and click Open

    Mac/Linux:
     * Open terminal and type (using the Pi's IP address):

    .. code-block:: bash

      ssh pi@192.168.1.123

11. Doing so will prompt you to enter the Pi's new password. Enter it.

.. note:: The default port used by Pi for SSH is 22. As long as your router
          and Pi password are strong, the security risk is minimized.
          Currently, SSH will only allow you to access the Pi when your
          computer and the Pi are connected to the same router.

Desktop Interface
-----------------
Sometimes an terminal only interface does not suffice. We can alternatively
connect to the Raspberry Pi using a VNC (Virtual Network Computing) Viewer to
see the 'screen' of the Pi.

Procedure
^^^^^^^^^
1. Login to the Pi as usual using SSH
2. Enable VNC by using the following command:

   .. code-block:: bash

     sudo raspi-config

   * Navigate to ``Interfacing Options`` >> ``VNC`` >> ``Enable``

3. Reboot the Pi

   .. code-block:: bash

       sudo reboot now

4. Install `VNC Viewer <https://www.realvnc.com/en/connect/download/vnc/>`_
   on your laptop.
5. Open VNC viewer. Open a new connection: ``File`` >> ``New Connection``

   *  Use the local IP of the Pi and the SSH port (22 by default)
   *  Use your credentials to login

6. You should be able to see the same screen that you saw when you initially connected to the Pi using HDMI

.. note:: For SSH connection to work, your laptop needs to be connected to the same WiFi (router) that the Raspberry Pi
          is connected to.

Password-less SSH
-----------------
For SHH via a private computer, you can use an SSH key pair to login to the
server or Raspberry Pi without a password

Procedure
^^^^^^^^^
1. Open a new terminal window and type the following command to generate a
   SSH key pair. You will keep the private key on your computer and send the
   public key to the server which will authenticate SSH connection without the
   password.

   .. code-block:: bash

    ssh-keygen -t rsa

    * Follow through the process. If key pair has been generated previously,
    choose a new file name. A passphrase is not necessary.

2. The following commands will create a SSH directory on the Pi, upload the
   generated public key to to the Pi and set the necessary permissions (replace
   ``<Pi IP Address>``, ``<Pi SSH Port (defaut: 22)>`` and ``<Pi username>``
   with their respective names/numbers):

   .. code-block:: bash

      ssh_ip=<Pi IP Address>
      ssh_port=<Pi SSH Port (defaut: 22)>
      ssh_user=<Pi username>

      ssh $ssh_user@$ssh_ip -p $ssh_port mkdir -p .ssh
      cat ~/.ssh/id_rsa.pub | ssh $ssh_user@$ssh_ip -p $ssh_port 'cat >> .ssh/authorized_keys'
      ssh $ssh_user@$ssh_ip -p $ssh_port "chmod 700 .ssh; chmod 640 .ssh/authorized_keys"

   .. note:: You will need to enter the SSH password for the above steps. Also,
             there is no space between ``ssh_pi``, ``=`` and ``<Pi IP Address>``, etc.

3. Now the SSH keys have been set up. To make the connecting via SSH even
   faster, do the following:

   .. code-block:: bash

      cat ~/.ssh/config

   * If the ``~/.ssh/config`` file does not exist, create one using ``nano``:

   .. code-block:: bash

      sudo nano ~/.ssh/config

   * Fill it in the following format:

   .. code-block:: bash

      Host <some unique name>
         Hostname <Pi IP Address>
         User <Pi username>
         Port <Pi SSH Port (defaut: 22)>

   * Or you can use the following command:

   .. code-block:: bash

      ssh_id=<some unique name>
      echo "\nHost $ssh_id\n   Hostname $ssh_ip" >> ~/.ssh/config
      echo "\n   User $ssh_user\n   Port $ssh_port" >> ~/.ssh/config

   * Example (in ``~/.ssh/config``):

   .. code-block:: bash

      Host pi-server
         Hostname 192.168.1.200
         User pi
         Port 22

   * Save the file

4. Now you can SSH in to the Pi without a password using the command:

   .. code-block:: bash

      ssh pi-server # or whatever host identifier you chose





Resources
---------
- `Adafruit's Raspberry Pi Tutorial <https://learn.adafruit.com/series/learn-raspberry-pi>`_
- `Instructables Raspberry Pi Projects <http://www.instructables.com/howto/?sort=none&q=raspberry+pi>`_
