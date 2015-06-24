# -*- coding: utf-8 -*-
"""
Homeshick castle which reimplements (some of) the features of homeshick
"""
import logging
import os
import os.path
import pathlib
from homeslick.castle import Castle

DEV_LOGGER = logging.getLogger(__name__)

def _is_link_to(test_path, dest_path):
    '''
    Return true if test_path is a symlink that points to dest_path
    '''
    try:
        resolved_dest_path = dest_path.resolve()
    except FileNotFoundError as resolve_dest_exception:
        try:
            test_path.resolve()
        except FileNotFoundError as resolve_test_exception:
            return resolve_test_exception.filename == resolve_dest_exception.filename
        else:
            return False
    else:
        try:
            resolved_test_path = test_path.resolve()
        except FileNotFoundError:
            return False
        else:
            return resolved_dest_path == resolved_test_path


class Homeshick(Castle):
    """
    Homeshick castle which reimplements (some of) the features of homeshick
    """
    def pull(self):
        super().pull()
        self.symlink()

    def init(self):
        super().init()
        self.symlink()

    def _symlink_iterator(self, castle_path, home_path):
        for sub_path in castle_path.iterdir():
            castle_sub_path = sub_path
            home_sub_path = home_path / sub_path.name
            yield castle_sub_path, home_sub_path

            if sub_path.is_dir():
                yield from self._symlink_iterator(castle_sub_path, home_sub_path) # NOQA

    def _symlink_directory(self, castle_path, home_path):
        '''
        Handle symlinking for case where castle entry is a directory
        '''
        self.log.debug('Handling directory %s', castle_path)
        if _is_link_to(home_path, castle_path):
            self.log.debug('Symlink already exists for %s', home_path)
            return

        if home_path.exists():
            if home_path.resolve().is_dir():
                return
            else:
                # Otherwise conflict.. which we havent coded for yet
                raise NotImplementedError('Conflict')
        else:
            self.log.debug('Creating directory %s', home_path)
            home_path.mkdir()
            return

    def _symlink_file(self, castle_path, home_path):
        '''
        Handle symlinking for case where castle entry is file
        '''
        self.log.debug('Handling file %s', castle_path)

        if _is_link_to(home_path, castle_path):
            self.log.debug('Symlink already exists for %s', home_path)
            return

        if home_path.exists():
            # Otherwise conflict.. which we havent coded for yet
            raise NotImplementedError('Conflict')
        else:
            self.log.debug('Creating symlink from %s to %s', castle_path, home_path)
            home_path.symlink_to(castle_path)

    def symlink(self):
        '''
        Symlink from homeshick to home

        Behaviour stolen from https://github.com/andsens/homeshick/wiki/Symlinking
        '''
        self.log.info('Symlinking')

        symlink_iter = self._symlink_iterator(
            self._staging_path / 'home', self._global_context.home_path)

        for castle_path, home_path in symlink_iter:
            self.log.debug('Comparing %s and %s', castle_path, home_path)
            if castle_path.is_dir():
                self._symlink_directory(castle_path, home_path)
            else:
                self._symlink_file(castle_path, home_path)
