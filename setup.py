#!/usr/bin/env python

from setuptools import setup

exec(open('pymailgen/version.py').read())
setup(
    name='pymailgen',
    version=__version__
)
