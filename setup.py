#!/usr/bin/env python2

from setuptools import setup, find_packages
import sys

setup(
    zip_safe=True,
    use_2to3=False,
    name='mdclear',
    version='0.0.1',
    long_description='Clear Maven metadata related to a PNC build from an Indy repository manager',
    classifiers=[
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: Apache Public License v2 (APL)",
      "Programming Language :: Python :: 3",
      "Topic :: Software Development :: Build Tools",
      "Topic :: Utilities",
    ],
    keywords='indy PNC build java ',
    author='John Casey',
    author_email='jdcasey@commonjava.org',
    url='https://github.com/Commonjava/pnc-metadata-clear',
    license='APLv2+',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=[
      "requests",
      "ruamel.yaml",
      "click"
    ],
    entry_points={
        'console_scripts': [
            'pnc-clear-metadata = mdclear:run'
        ],
    }
)

