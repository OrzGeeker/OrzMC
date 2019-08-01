# !/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestSuite, makeSuite, TextTestRunner
from Mojang import TestMojang

if __name__ == "__main__":
    suite = TestSuite()
    suite.addTest(makeSuite(TestMojang))
    TextTestRunner(verbosity=2).run(suite)