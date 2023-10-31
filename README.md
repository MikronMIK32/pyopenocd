# Python OpenOCD wrapper

This is a simple module for interfacing with openocd via TCL api.

## Installation

    pip install git+https://github.com/MikronMIK32/pyopenocd

## Usage

    >>> from openocd import OpenOcdTclRpc
    >>> with OpenOcdTclRpc() as openocd:
    ...     print(openocd.run('expr 1 + 1'))
    ...
    2

## Command line

The openocd module is executable and can serve as a simple openocd remote from
shell scripts:

    $ openocd-remote run expr 1 + 2
    3
    $ openocd-remote run targets
    ...

## Testing

pytest and tox are used for testing. Most useful tests require openocd to be running but
they are skipped by default unless --openocd-running is passed on cmdline:

    tox -- --openocd-running
