#!/usr/bin/env python

from setuptools import setup, find_packages
setup(
    name='pnprma',
    version='1.0',
    author='PNP@Cisco',
    author_email='pnp-support@cisco.com',
    description='Tool for RMAing Cisco Devices using PnP',
    packages=find_packages(),
    install_requires=['flask', 'flask-cors', 'paramiko'],
    entry_points={
        'console_scripts': [
            'pnp-rma=pnprma.app:main'],
    }
)