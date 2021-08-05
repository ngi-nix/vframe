#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='TODO-name',
      version='1.0',
      # Modules to import from other scripts:
      packages=find_packages(),
      # Executables
      scripts=["vframe_cli/cli.py"],
     )
