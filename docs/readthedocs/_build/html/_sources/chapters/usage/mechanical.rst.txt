Mechanical
=================

The mechanical documentation involves designing, 3D printing and assembling
the PiCar chassis

Design
------
For the base chassis of PiCar v2, we will be using the Dromida 1/18 Scale
Buggy. It retrofit it with sensors and micro-controllers, we will be adding
some 3D printed parts.

CAD
^^^^^^
The parts are designed using `Autodesk Fusion 360
<https://www.autodesk.com/products/fusion-360>`_. We will be splitting the
chassis into three layers, connected with spacers for better management:

Layer Zero
  - Dromida buggy (without cover)
  - DC Motor (drive)
  - Servo (steer)
  - Encoder
  - ESC

Layer One
  - Raspberry Pi
  - Arduino
  - Lipo Battery(s)
  - Current sensors
  - IMU

Layer Two
  - Servo (LIDAR)
  - TFMini LIDAR
  - PiCamera

Assembly
--------


Materials Required
^^^^^^^^^^^^^^^^^^
.. csv-table::
   :header-rows: 1
   :file: mechanical/bill_of_materials.csv
