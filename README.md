Raspberry Pi Car Project
========================

The Raspberry Pi Car project aims to design a miniature four-wheeled car powered by a Raspberry Pi 3 board. This lab-scale autonomous research platform is easy to build and modify. A camera mounted on the car allows for complex computer vision algorithms. 

This repository contains all the software and hardware source files required to duplicate the car, including:
* Chassis 3D printer CAD sources.
* Raspberry Pi 3 breakout PCB to connect peripherals and draw power from LiPo battery.
* Source code of the following sofware modules capable of:
 * Acquire wheel angle data from two quadrature encoders.
 * Acquire acceleration, angular velocity, and compass data from an I²C LSM9DS1 IMU.
 * Acquire video data from a Raspberry Pi NoIR camera.
 * Acquire position and angle data from a motion-capture server.
 * Control the speed of two brushless DC motors.
 * Control an I²C 8x8 LED matrix.
