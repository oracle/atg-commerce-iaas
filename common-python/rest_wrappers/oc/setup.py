#!/usr/bin/python
# Copyright (c) 2013, 2014-2016 Oracle and/or its affiliates. All rights reserved.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Andrew Hopkinson (Oracle Cloud Solutions A-Team)"
__copyright__ = "Copyright (c) 2013, 2014-2016  Oracle and/or its affiliates. All rights reserved."
__ekitversion__ = "@VERSION@"
__ekitrelease__ = "@RELEASE@"
__version__ = "1.0.0.0"
__date__ = "@BUILDDATE@"
__status__ = "Development"
__module__ = "setup"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys

setup(name             = 'oc',
      version          = __version__,
      description      = 'Oracle Compute Cloud Service REST API wrappers',
      author           = __author__,
      url              = 'https://support.oracle.com/epmos/faces/SearchDocDisplay?_adf.ctrl-state=dshlcolsc_9&_afrLoop=462772069085422',
      packages         = ['oc'],
      classifiers      = [
          'Development Status :: 3 - Alpha',

          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',

          'Operating System :: OS Independent',

          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python'
      ],
      install_requires = [
          'simplejson',
          'requests'
      ]
      )
