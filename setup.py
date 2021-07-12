#!/usr/bin/env python3
from setuptools import setup, find_packages
import os

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='episimmer',
    version='0.1.0',
    description='Epidemic Simulation Platform',
    long_description=readme,
    author='HealthBadge',
    author_email='episimmer@healthbadge.org',
    url='https://github.com/healthbadge/episimmer',
    license=license,
    packages=find_packages(exclude=('tests', 'docs', 'examples')),
    install_requires=required
)
