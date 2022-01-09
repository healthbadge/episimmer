import os
import sys

from pkg_resources import DistributionNotFound, get_distribution

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(PROJECT_PATH, 'src')
sys.path.append(SOURCE_PATH)

# try:
#     __version__ = get_distribution('episimmer').version
# except DistributionNotFound:
#     raise DistributionNotFound('Please install the package using setup.py')
