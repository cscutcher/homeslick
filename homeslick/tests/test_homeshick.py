# -*- coding: utf-8 -*-
"""
Test Homeshick object
"""
import logging
import unittest
import os
import tempfile
from homeslick import context
from homeslick.homeshick import Homeshick

DEV_LOGGER = logging.getLogger(__name__)


class TestHomeshick(unittest.TestCase):
    '''
    Test Castle object
    '''
    TEST_NAME = 'temp'
    TEST_GIT_URI = 'https://github.com/cscutcher/safe_home.git'

    def setUp(self):
        self._fake_home = tempfile.TemporaryDirectory(suffix='homeslick_castle_test')
        self._old_context = context.get_context()
        self._old_home = os.environ['HOME']
        os.environ['HOME'] = self._fake_home.name
        context.update_context(context.Context())
        self.castle = Homeshick(self.TEST_NAME, self.TEST_GIT_URI)

    def tearDown(self):
        context.update_context(self._old_context)
        os.environ['HOME'] = self._old_home
        #self._fake_home.cleanup()

    def test_symlink(self):
        self.castle.init()
        self.castle.symlink()

    def test_symlink_twice(self):
        '''
        Test symlink twice doesn't cause conflict
        '''
        self.castle.init()
        self.castle.symlink()
        self.castle.symlink()
