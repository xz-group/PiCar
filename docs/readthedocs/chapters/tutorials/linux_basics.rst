Linux Basics
=============

What is Linux?
--------------
Linux is an open-source operating system. It is the underlying operating
system on which many popular operating systems like Android, Ubuntu, Raspbian
and MacOS are based on.

Getting started
---------------
General Linux Commands
^^^^^^^^^^^^^^^^^^^^^^
1. SSH into a Raspberry Pi or use a computer with Ubuntu.
2. Try out the following commands in the terminal:

Make (create) directory with name ``foo``
 .. code-block:: bash

    mkdir foo

List Files
  .. code-block:: bash

     ls

Change directory to ``foo``
  .. code-block:: bash

     cd

Print Working Directory
  .. code-block:: bash

     pwd

Create Python script
  .. code-block:: bash

     nano helloworld.py

.. note:: ``nano`` is the simplest Terminal based editor you can use. You
          can also use ``vi``. If you are on the Desktop (via HDMI or VNC),
          you can use graphical editors like ``gedit`` and ``Atom``.


Within ``helloworld.py``, type the following:
  .. code-block:: python

     print("Helloworld!")

  * Save the file using ``Ctrl + X`` >> ``Y`` >> ``Enter``

Run the Python script
  .. code-block:: bash

     python helloworld.py

  * This should output ``HelloWorld!``

Concatenate (get contents) of a file
  .. code-block:: bash

     cat helloworld.py

  * This should output ``print("Helloworld!")``

Copy file ``helloworld.py`` to ``copy_of_helloworld.py``
  .. code-block:: bash

     cp helloworld.py copy_of_helloworld.py

  * Try ``ls`` now.

Move file (``copy_of_helloworld.py``) to new directory ``bar``
  .. code-block:: bash

     mkdir bar
     mv copy_of_helloworld.py bar/

.. note:: Sometimes, typing the entire filename or command takes too long. In
          cases like this you can use ``Tab Completion`` to quickly type the
          commands. You write the partial file/directory name or command and
          press ``Tab`` to complete it (or choose from possible options by
          double tapping ``Tab``).

.. note:: Use the ``UP Arrow Key`` to use the fetch the previously used command.

Rename file (``copy_of_helloworld.py``) to (``renamed_helloworld.py``)
  .. code-block:: bash

     cd bar/
     mv copy_of_helloworld.py renamed_helloworld.py

Go back a directory level
  .. code-block:: bash

     cd ..

Delete a file or directory
  .. code-block:: bash

     rm bar/renamed_helloworld.py
     rm bar -R

Manual for a command
  .. code-block:: bash

     man rm
     man sudo

Update and upgrade your Linux packages
  .. code-block:: bash

     sudo apt-get update
     sudo apt-get upgrade

.. note:: ``sudo`` is akin to an admin. Using it will sometimes ask you to
          enter the user's password.

Installing a new package like ``htop``
  .. code-block:: bash

     sudo apt-get install htop
     htop

.. note:: ``htop`` is a great terminal way of checking how much
          processing power and memory your computer is using.

Pinging a website like ``www.google.com``
  .. code-block:: bash

     ping www.google.com

Show network configuration
 .. code-block:: bash

    ifconfig
    iwconfig

Check date
  .. code-block:: bash

     date

Clear screen
  .. code-block:: bash

     clear

Check version of an installed package
 .. code-block:: bash

    htop -v

Get local and global IP
 .. code-block:: bash

    hostname -I
    curl ifconfig.me

Disk space information
 .. code-block:: bash

    df -h

Raspberry Pi Specific Commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Check the pinouts on the Raspberry Pi
  .. code-block:: bash

     pinout
     gpio readall

Lists connected USB hardware
  .. code-block:: bash

     lsusb

Show Raspberry Pi CPU Temperature
  .. code-block:: bash

     vcgencmd measure_temp

Show CPU & GPU memory split
  .. code-block:: bash

     vcgencmd get_mem arm && vcgencmd get_mem gpu

.. note:: If you need more than one ``Terminal`` open at one time, and you
          do not want too many new Terminal windows, you can use ``Ctrl`` +
          ``Shift`` + ``T``.

Resources
---------
- `Digital Ocean's Linux Intro <https://www.digitalocean.com/community/tutorials/an-introduction-to-linux-basics>`_
- `Fundamental and common Linux commands
  <https://www.raspberrypi.org/documentation/linux/usage/commands.md>`_
