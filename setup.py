#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sys 
from setuptools import setup 
from setuptools.command.test import test as TestCommand 

class PyTest(TestCommand): 
    '''pytest's integration with setuptools, which is borrowed from  
    http://pytest.org/latest/goodpractises.html#goodpractises
    '''

    def finalize_options(self): 
        TestCommand.finalize_options(self)
        self.test_args = [] 
        self.test_suite = True 

    def run_tests(self): 
        import pytest 
        errcode = pytest.main(self.test_args) 
        sys.exit(errcode) 

setup(
    name           = 'basket', 
    version        = '0.0.1', 
    author         = 'Zhi Yang', 
    packages       = ['basket', 'test'], 
    tests_require  = ['pytest'], 
    entry_points   = {'console_scripts': ['blackjack = basket.cli:main']}, 
    cmdclass       = {'test': PyTest}, 
    test_suite     = 'test', 
    extras_require = {'testing': ['pytest']} 
)

