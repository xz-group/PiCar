Getting Started
===============

The PiCar project is a miniature four-wheeled car powered by a Raspberry Pi 3
board. This lab-scale autonomous research platform is easy to build and modify.
A camera and LIDAR mounted on the car allows for complex computer vision
algorithms.

.. raw:: html

  <p align="middle">
  <a href="https://github.com/xz-group/PiCar" target="_blank"
  class="btn btn-neutral" title="Go to the PiCar Repo">
  <span class="icon icon-github"></span> PiCar GitHub</a>
  &nbsp;
  <a href="../index.html" target="_blank"
  class="btn btn-neutral" title="Go to the Table of Contents">
  <span class="fa fa-navicon"></span> Table of Contents</a></p>


The `PiCar GitHub Repository <https://github.com/xz-group/PiCar>`_ contains
all the software and hardware source files required to duplicate the car,
including:

  *  Chassis 3D printing, and CAD sources.
  *  Raspberry Pi 3 breakout PCB to connect peripherals and draw power from
     LiPo battery (v1).
  *  Source code for intergrating sensors like the encoder, IMU, Lidar and
     camera
  *  Source code for controlling the PiCar, networking, computer vision, etc.

The purpose of this documentation is to create a full fledged, clear formal
guide for using the PiCar project. It will also serve as a place for showcasing
results.

**Where to begin:**

1. A good place to start is to think about what you want your robot to do. The
PiCar is intended to be a inexpensive way to build a robust mobile robot
capable of running complex algorithms.

2. `Usage -> Mechanical <usage/mechanical.html>`_ has a list of parts you would
need to build the PiCar. It also contains instructions on how to assemble the
PiCar.

.. note::

  For your particular project, you may not need all the parts to
  assemble the PiCar.

  - If the ``Dromida Buggy`` is not available, you may consider
    buying other similaryly sized (1/18th scale) chassis.
  - If you are looking for having higher computational power, you could replace
    the ``Raspberry Pi`` with something like the ``NVidia Jetson TX2``.
  - You may not need the ``Current Sensors`` for your project.
  - You could substitute the ``TFMini Lidar`` with a more powerful one like the
    ``YDLidar F4`` or a less powerful one like the ``SR05 Ultrasonic sensor``.

3. On the software side of things, we currently use ``Python 3`` as the
primary programming language for the ``Raspberry Pi``. ``Arduino`` uses
``Arduino C``. If you are unfamiliar with any of these hardware or software,
the `Tutorials <tutorials.html>`_ section is a great place to start. The
`PiCar GitHub Repository <https://github.com/xz-group/PiCar>`_ contains all the
code and also houses this documentation.

4. Once the PiCar has been assembled, the `Usage <usage.html>`_  secrtion has
information about how the different modules work and how they can be controlled.
It also has information about the ``PiCar Module`` or Class that is used for
controlling any aspect of the PiCar.

5. If you would like to add your results to the `Results <results.html>`_ page,
kindly let us know. For contributing directly to the project, either by
fixing or updating the codebase or documentation, kindly submit a `GitHub pull
request <https://github.com/xz-group/PiCar/pulls>`_.
