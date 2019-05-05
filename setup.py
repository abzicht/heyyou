import os
import sys
from pathlib import Path

from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)
"""
parts of this setup script are proudly copied from DJANGO
"""
# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of backback requires Python {}.{}
""".format(REQUIRED_PYTHON[0], REQUIRED_PYTHON[1]))
    sys.exit(1)


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


home = str(Path.home())

setup(
    name='heyyou',
    version="0.0.1",
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    author='Abzicht',
    author_email='abzicht@gmail.com',
    description=('A simple script demonstrating the power that comes with SSID sniffing'),
    long_description=read('README.md'),
    license='mit',
    include_package_data=False,
    packages=find_packages(),
    entry_points={'console_scripts': [
        'heyyou = heyyou.script:main',
    ]},
    install_requires=['argparse', 'requests', 'scapy'],
)
