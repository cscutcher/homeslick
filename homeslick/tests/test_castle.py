# -*- coding: utf-8 -*-
"""
Test Castle object
"""
import logging
import unittest
import os
import tempfile
from homeslick import context
from homeslick.castle import Castle
from homeslick.castle import CastleState
from homeslick.castle import InvalidCastleStateError

DEV_LOGGER = logging.getLogger(__name__)


class TestCastle(unittest.TestCase):
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
        self.castle = Castle(self.TEST_NAME, self.TEST_GIT_URI)

    def tearDown(self):
        context.update_context(self._old_context)
        os.environ['HOME'] = self._old_home
        self._fake_home.cleanup()

    def test_missing(self):
        self.assertEqual(self.castle.get_status(), CastleState.missing)

    def test_clone(self):
        self.castle._clone()
        self.assertEqual(self.castle.get_status(), CastleState.fresh)

    def test_fetch(self):
        '''
        Test fetch.
        TODO: This only tests it runs without exceptions. Need some assertions
        '''
        self.castle._clone()
        self.castle._fetch()

    def test_outdated(self):
        '''
        Test that we can detect outdated commit
        '''
        self.castle._clone()

        # Reset to old revision
        self.castle._get_git_repo().head.reset(commit='HEAD^', working_tree=True)

        self.assertEqual(self.castle.get_status(), CastleState.outdated)

    def test_double_clone(self):
        '''
        Test double cloning causes exceptions
        '''
        self.castle._clone()
        self.assertEqual(self.castle.get_status(), CastleState.fresh)
        castle = Castle(self.TEST_NAME, self.TEST_GIT_URI)
        with self.assertRaises(InvalidCastleStateError):
            castle._clone()
