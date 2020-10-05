#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='episimmer',
    version='0.1.0',
    description='Epidemic Simulation',
    long_description=readme,
    author='Corollary',
    author_email='team@corollary.com',
    url='https://github.com/corollary-health/episimmer',
    license=license,
    packages=find_packages(exclude=('tests', 'docs', 'examples'))
)