Object Tracking in Low-Power Autonomous Systems
================================================

Proposal
---------

  Computer vision algorithms are typically reserved for platforms that can
  handle the computational workload needed to process the huge amount of data
  in images and videos. The recent surge in artificial intelligence, machine
  learning, and computer vision have guided the development of powerful
  processors that can quickly and more efficiently handle the computationally
  intensive algorithms.  For this project, I aimed to go against the grain and
  implement computer vision and artificial intelligence on a Raspberry Pi, a
  low-power IoT device that is the on-board processor for a small autonomous
  vehicle project called the PiCar.

  The first part of the project was the development and implementation of a
  real-time control algorithm using optical flow and machine learning to
  successfully navigate randomly generated obstacle fields. The processing was
  done entirely on a Raspberry Pi 3 and the video stream was provided from the
  standard Raspberry Pi camera module. The algorithm worked in the following
  manner:

  1. Read images from video stream
  2. Detect features using Shi-Tomasi corner detection
  #. Calculate optical flow vectors
  #. Calculate time to contact (TTC) for each tracked point (x,y)
  #. Cluster three dimensional data (x,y,TTC) using DBSCAN
  #. Sort clusters by lowest TTC
  #. Calculate servomotor angle and motor PWM
  #. Send signal to motor-controller via SPI

Authors
-------

- `William Luer <https://github.com/willluer>`_

Links
-----

[`Report <https://github.com/xz-group/PiCar/blob/master/docs/reports/optical_flow_luer_2018/optical_flow_luer_2018.pdf>`_]
[`Code <https://github.com/xz-group/PiCar/tree/master/src/pi/computer_vision>`_]
