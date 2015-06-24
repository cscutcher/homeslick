# -*- coding: utf-8 -*-
"""
Context Utility
"""
import logging
import os
from pathlib import Path

DEV_LOGGER = logging.getLogger(__name__)


class Context(object):
    '''
    Store context for homeslick
    '''
    APP_NAME = 'homeslick'

    def __init__(self):
        self._home_path_override = None
        self._castles_path_override = None
        self._config_path_override = None

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return (
            '{self.__class__.__name__}('
            'home_path={self.home_path!r}, '
            'castles_path={self.castles_path!r}, '
            'config_path={self.config_path!r})'.format(self=self))

    @property
    def home_path(self):
        if self._home_path_override is None:
            return Path(os.environ['HOME'])
        else:
            return self._home_path_override

    @home_path.setter
    def home_path(self, value):
        self._home_path_override = Path(value)

    @property
    def castles_path(self):
        if self._castles_path_override is None:
            return self.home_path / '.local' / 'share' / self.APP_NAME / 'castles'
        else:
            return self._castles_path_override

    @castles_path.setter
    def castles_path(self, value):
        self._castles_path_override = Path(value)

    @property
    def config_path(self):
        if self._config_path_override is None:
            return self.home_path / '.config' / self.APP_NAME / 'config.yml'
        else:
            return self._config_path_override

    @config_path.setter
    def config_path(self, value):
        self._config_path_override = Path(value)

_CONTEXT = None


def get_context():
    '''
    Get context utility
    '''
    global _CONTEXT
    if _CONTEXT is None:
        _CONTEXT = Context()
    return _CONTEXT


def update_context(context):
    '''
    Replace global context

    Returns existing context
    '''
    global _CONTEXT

    old_context = _CONTEXT
    _CONTEXT = context

    return old_context
