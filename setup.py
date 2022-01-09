from setuptools import find_packages, setup

NAME = 'episimmer'
VERSION = '2.0.0'
DESCRIPTION = 'Epidemic Simulation Platform'
URL = 'https://github.com/healthbadge/episimmer'
EMAIL = 'inavamsi@healthbadge.org, surya@healthbadge.org'
AUTHOR = 'Inavamsi Enaganti, Surya Dheeshjith'
LICENSE = 'BSD-3-Clause'
PYTHON = '>=3.7'
CLASSIFIERS = [
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Topic :: Scientific/Engineering',
]
ENTRY={
    'console_scripts': [
        'episimmer=src.Main:main',
    ]
}

with open('README.md') as f:
    LONG_DESC = f.read()

with open('requirements.txt') as f:
    REQUIRES = f.read()

with open('docs/requirements-dev.txt') as f:
    DEV_REQUIRES = f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESC,
    entry_points=ENTRY,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    install_requires=REQUIRES,
    extras_require={'test': DEV_REQUIRES},
    packages=find_packages(exclude=['tests', 'docs', 'examples'])
)
