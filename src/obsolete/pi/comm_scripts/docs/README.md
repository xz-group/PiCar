This directory contains general documentation for the project.
For method/class specific documentation, see the source files.

This project was designed so that any user can imply add
`from core.network import Network` to the top of any Python script and
instantly start networking between an arbitrary number of Raspberry Pis (minus
some setup). For an example of how to use the networking class, see
`../experiments/driver/full_test/master.py` and `slave.py`. The `master.py`
script contains an example of the `Network` sending, and the `slave.py` script
and example of it receiving.