#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='beam',
    version='0.1.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: Apache Software License',
    ],
    packages=find_packages(),
    scripts=[
        'scripts/run.py'
    ]
)
