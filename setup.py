#!/usr/bin/env python3

from setuptools import find_packages, setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


install_requires = [
    'matplotlib==3.4.2'
    'numpy==1.17.2'
    'pyvis==0.1.9'
]
tests_require = ['pytest', 'pytest-cov']
dev_requires = tests_require + ['pre-commit']


setup(
    name='episimmer',
    version='0.1.0',
    description='Epidemic Simulation Platform',
    long_description=readme,
    author='HealthBadge',
    author_email='episimmer@healthbadge.org',
    url='https://github.com/healthbadge/episimmer',
    license=license,
    python_requires='>=3.8',
    install_requires=install_requires,
    extras_require={
        'test': tests_require,
        'dev': dev_requires,
        },
    packages=find_packages(exclude=('tests', 'docs', 'examples')),
    include_package_data=True
    )
