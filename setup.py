# -*- coding: utf-8 -*-
"""
Setup for homeslick
"""
import sys

MIN_PYTHON_VERSION = (3, 0)
if sys.version_info <= MIN_PYTHON_VERSION:
    raise EnvironmentError(
        'Homeslick was built for python {0} found {1}'.format(
            MIN_PYTHON_VERSION,
            sys.version_info))


from setuptools import setup, find_packages

setup(
    name="homeslick",
    version="0.1",
    packages=find_packages(),
    install_requires=('pathlib', 'appdirs', 'gitpython>=0.3'),
)
