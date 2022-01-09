from setuptools import find_packages, setup
import os.path as osp

NAME = 'episimmer'
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

with open(osp.join("episimmer", "version.txt")) as f:
    VERSION = f.read().strip()

with open('README.md') as f:
    LONG_DESC = f.read()

with open('requirements.txt') as f:
    REQUIRES = f.read()

with open('docs/requirements-dev.txt') as f:
    DEV_REQUIRES = f.read()

LONG_DESC_CONTENT_TYPE = 'text/markdown'
EXTRA_REQUIRES = {'test': DEV_REQUIRES}

ENTRY={
    'console_scripts': [
        'episimmer=episimmer.main:main',
    ]
}
EXCLUDES = ['tests*','scripts']


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type=LONG_DESC_CONTENT_TYPE,
    long_description=LONG_DESC,
    entry_points=ENTRY,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    install_requires=REQUIRES,
    extras_require=EXTRA_REQUIRES,
    packages=find_packages(exclude=EXCLUDES)
)
