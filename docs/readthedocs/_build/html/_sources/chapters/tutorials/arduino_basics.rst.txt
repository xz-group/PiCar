Arduino Basics
=================

A small crash course on the Arduino micro-controller.

What is an Arduino?
-------------------
`Arduino <https://www.arduino.cc/>`_  is an open-source electronics platform
based on easy-to-use hardware and software. It's intended for anyone making
interactive projects. We will be using the Arduino micro-controller to
interface with the motor and servo(s).

Getting Started
----------------
Materials Required
^^^^^^^^^^^^^^^^^^^
- `Arduino UNO <https://store.arduino.cc/usa/arduino-uno-rev3>`_
- UNO compatible USB cable
- A laptop or computer for programming the Arduino

Procedure
^^^^^^^^^
1. Download and install the
   `Arduino IDE <https://www.arduino.cc/en/Main/Software>`_ (Integrated
   development environment) for your OS

2. Launch the Arduino IDE.

3. Connect the Arduino UNO to your computer via a USB cable.

4. Go to ``File`` >> ``Examples`` >> ``01. Basics`` >> ``Blink``

5. Choose the correct board by navigating to ``Tools`` >> ``Board`` >>
   ``Arduino/Genuino UNO``

6. Choose the correct board by navigating to ``Tools`` >> ``Port`` >>
   ``COMx (Arduino UNO)`` on Windows or ``/dev/ttyACMx`` on Linux

7. Click the ``Upload`` button (arrow pointing to the right).

8. You should see that the on-board LED on the Arduino (pin 13) blinks every
   second.

9. You can also hook up an external LED to the GND and digital pin 13 to make
   the that LED blink.

10. Try changing ``delay(1000)`` to ``delay(3000)`` and see what happens

11. You have successfully completed your first Arduino program.

Todo
-----
- Fetch sensor data
- Program servo

Resources
---------
- `LadyAda's Arduino tutorial <http://www.ladyada.net/learn/arduino/>`_
- `Adafruit's Arduino tutorial <https://learn.adafruit.com/lesson-0-getting-started>`_
- `Instructables Arduino projects <http://www.instructables.com/howto/arduino/>`_
