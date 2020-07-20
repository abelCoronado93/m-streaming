#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Setup file.
"""

from __future__ import print_function
from setuptools import setup, find_packages

__author__ = 'Abel Coronado López'
__email__ = 'abel.coronado@pragsis.com'

setup(
    name='m_streaming',
    version='0.0.1',
    author='Abel Coronado López',
    author_email='abel.coronado@pragsis.com',
    url='abel.coronado@estudiante.uam.es',

    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'pyspark==2.4.4',
        'py4j==0.10.7',
        'PyYAML',
        'snappy'
    ],

    test_suite='tests',
    tests_require=[
        'pytest==5.2.3',
        'pytest-cov==2.8.1',
        'pylint==2.4.4',
        'pyspark==2.4.4'
    ],

    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Unix'
    ],
    entry_points={

    },
    include_package_data=True,
    zip_safe=True
)