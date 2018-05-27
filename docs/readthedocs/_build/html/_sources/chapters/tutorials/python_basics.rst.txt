Python Basics
======================

What is Python?
----------------------
`Python <https://www.python.org/>`_ is a programming language that lets you
work quickly and integrate systems more effectively. We will be using it for
programming the Raspberry Pi, data aggregation, data transfer and data anaylsis.
`Python 2.7 <https://www.python.org/downloads/release/python-2715/>`_ and
`Python 3 <https://www.python.org/downloads/release/python-365/>`_ are the
most popular versions of Python.

Installation
-----------------------
Windows
    - Download and install the Python setup from `Python Releases for
      Windows <https://www.python.org/downloads/windows/>`_
    - Download `Eclipse <https://www.eclipse.org/downloads/>`_ or a similar IDE
      and follow this `tutorial for setting up Python on Eclipse
      <https://www.rose-hulman.edu/class/csse/resources/Eclipse/eclipse-python-configuration.htm>`_

Mac
    - Python 2.7 comes pre-installed with the Mac OS X 10.8 +.
    - To install and use other versions of Python on a Mac, use the tutorial on
      `Using Python on a Macintosh <https://docs.python.org/3/using/mac.html>`_

Linux
    - Python (2.7 and 3.4) usually comes preinstalled with major distributions
      of Linux. You can test if Python is installed using the following commands
      in the terminal:

    .. code-block:: bash

       python --version
       python2 --version
       python3 --version

    - If you get a message saying no command found or package is missing, you can
      install it using:

    .. code-block:: bash

       sudo apt-get install python
       sudo apt-get install python3

HelloWorld with Python
----------------------
Create a new file called ``helloworld.py`` using the IDE for Windows/Mac
or using ``nano`` on Linux and enter the following Python code:

.. code-block:: python

   print("HelloWorld!")

Save and run the file. On the IDE it would be via clicking a ``Run Python Script``
button and via terminal you need to type ``python helloworld.py``.
The output should simply be the following:

.. code-block:: bash

   HelloWorld!

Installing Python Modules
-------------------------
What makes Python so powerful is the plethora of packages made to allow a
programmer do a lot of things like web-parsing, plotting, simulation,
computer vision, machine learning or simply getting the weather.
Use the official guide for `Installing Python Packages
<https://docs.python.org/3/installing/index.html>`_ to get things set up.

Windows
    - Use the ``py`` Python launcher in combination with the -m switch:

    .. code-block:: bash

       py -2   -m pip install SomePackage  # default Python 2
       py -2.7 -m pip install SomePackage  # specifically Python 2.7
       py -3   -m pip install SomePackage  # default Python 3
       py -3.4 -m pip install SomePackage  # specifically Python 3.4

Mac / Linux
    - Install ``pip`` which is a Python Package Installer

    .. code-block:: bash

       sudo apt-get install python-pip
       sudo apt-get install python3-pip

    - Install Python modules using ``pip``:

    .. code-block:: bash

       pip2 install SomePackage # short hand installation for Python 2
       pip3 install SomePackage # short hand installation for Python 2

       # or

       python2   -m pip install SomePackage  # default Python 2
       python2.7 -m pip install SomePackage  # specifically Python 2.7
       python3   -m pip install SomePackage  # default Python 3
       python3.4 -m pip install SomePackage  # specifically Python 3.4

.. note:: If you get an ``Permission denied`` while using ``pip``,
          you can append the command with ``--user``. Example: ``pip install
          matplotlib --user``. It is not recommended to use ``sudo`` to install
          packages using ``pip``.

.. note:: It is highly recommended to install the Python module called
          `IPython <http://ipython.org/>`_. It significantly improves upon the
          vanilla version of Python command line (terminal) interface.

Useful Modules
---------------
The `official list <https://wiki.python.org/moin/UsefulModules>`_ of useful
modules does not begin to cover the vast number of modules available for
different tasks, but it is a good place to start. Some of them are listed
below:

Computer Vision
^^^^^^^^^^^^^^^
- **openCV** (`<https://pypi.org/project/opencv-python/>`_)

Cloud Intergration
^^^^^^^^^^^^^^^^^^
- **Amazon Web Services** (`<https://aws.amazon.com/python/>`_)
- **Google Cloud** (`<https://googlecloudplatform.github.io/google-cloud-python/>`_)

GUIs (Graphical User Interfaces)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **PyGObject** (`<https://pygobject.readthedocs.io/en/latest/>`_)
- **tKinter** (`<https://docs.python.org/2/library/tkinter.html>`_)
- **wxPython** (`<https://wxpython.org/>`_)

Data Science & Scientific Computing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **NumPy** (`<http://www.numpy.org/>`_)
- **SciPy** (`<https://www.scipy.org/>`_)
- **pandas** (`<https://pandas.pydata.org/>`_)
- **parquet** (`<https://arrow.apache.org/docs/python/parquet.html>`_)

Interactive Python
^^^^^^^^^^^^^^^^^^
- **IPython** (`<http://ipython.org/>`_)
- **Jupyter Notebook** (`<http://ipython.org/>`_)

Games & Simulations
^^^^^^^^^^^^^^^^^^^
- **Pygame** (`<http://www.pygame.org/news.html>`_)
- **Pyglet** (`<http://www.pyglet.org/>`_)

Machine Learning
^^^^^^^^^^^^^^^^
- **TensorFlow** (`<https://www.tensorflow.org/install/>`_)
- **Keras** (`<https://keras.io/>`_)

Networking
^^^^^^^^^^
- **Twisted** (`<https://twistedmatrix.com/trac/>`_)

Plotting & Data-visualization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **matplotlib** (`<https://matplotlib.org/>`_)
- **seaborn** (`<https://seaborn.pydata.org/>`_)
- **plotly** (`<https://plot.ly/>`_)

Web Scraping
^^^^^^^^^^^^
- **BeautifulSoup** (`<https://www.crummy.com/software/BeautifulSoup/>`_)
- **Scrapy** (`<http://www.scrapy.org/>`_)

Miscellaneous
^^^^^^^^^^^^^
- **pint** (`<https://pint.readthedocs.io/en/latest/>`_)
     Define, operate and manipulate physical quantities

Resources
---------
- `Style Guide for Python <https://www.python.org/dev/peps/pep-0008/>`_
- `Automate the Boring Stuff <https://automatetheboringstuff.com/chapter1/>`_
