# -*- coding: utf-8 -*-
import unittest

class TestMojang(unittest.TestCase):
    def setUp(self):
        print('TestMojang Test setUp')

    def tearDown(self):
        print('TestMojang Test tearDown')


    def test_nothing(self):
        print('test nothing...')


if __name__ == "__main__":
    unittest.main()