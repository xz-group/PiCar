Datasheet
=================

RaspberryPi
-----------

RaspberryPi 3 B+
^^^^^^^^^^^^^^^^

*This section documents some information about the PI 3 MODEL B+ our team is using for easier reference.*

Check CPU information:

.. code-block:: bash

  lscpu

For the model we are using:

+-------------------+--------------------------------+
|Architecture       | armv7l                         |
+-------------------+--------------------------------+
|Byte Order         | Little Endian                  |
+-------------------+--------------------------------+
|CPU(s)             | 4                              |
+-------------------+--------------------------------+
|On-line CPU(s) list| 0-3                            |
+-------------------+--------------------------------+
|Thread(s) per core | 1                              |
+-------------------+--------------------------------+
|Core(s) per socket | 4                              |
+-------------------+--------------------------------+
|Socket(s)          | 1                              |
+-------------------+--------------------------------+
|Model              | 4                              |
+-------------------+--------------------------------+
|Model name         | ARMv7 Processor rev 4 (v7l)    |
+-------------------+--------------------------------+
|CPU max MHz        | 1400.0000                      |
+-------------------+--------------------------------+
|CPU min MHz        | 600.0000                       |
+-------------------+--------------------------------+
|BogoMIPS           | 38.40                          |
+-------------------+--------------------------------+
|Flags              | half thumb fastmult vfp edsp   |
|                   | neon vfpv3 tls vfpv4 idiva     |
|                   | idivt vfpd32 lpae evtstrm crc32|
+-------------------+--------------------------------+

**Important: Notice that the list says that the memory architecture is armv7l. However, on the raspberrypi 3 B+ official site, it says that the architecture is armv8. The diffrence is probably caused by the OS that the RaspberryPi is using(Raspbian). It is by default a 32bit system, and armv7 is 32bit while armv8 is 64bit, causing the architecture to adapt to 32bit**

For more information about this model, click `here <https://www.raspberrypi.org/documentation/hardware/raspberrypi/README.md>`_

Based on armv7l, the memory architecture for this model is:

+------------------------+------------------------------+
|L1-instruction Cache    | 32-bytes cache line size     |
|                        | 2-way set-associative Cache  |
+------------------------+------------------------------+
|L1-data Cache           | 64-bytes cache line size     |
|                        | 2-way set-associative cache  |
+------------------------+------------------------------+
|L2 Cache                | 128 KB in size               |
+------------------------+------------------------------+

*(However, in RaspberryPi, L2 Cache is devoted to GPU, the benefit and necessity of enabling it to data cache needs further exploration)*

Contributor: Jerry Kong
