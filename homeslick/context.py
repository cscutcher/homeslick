# -*- coding: utf-8 -*-
"""
Context Utility
"""
import logging
import os
from pathlib import Path
from appdirs import AppDirs

DEV_LOGGER = logging.getLogger(__name__)


class Context(object):
    '''
    Store context for homeslick
    '''
    def __init__(self):
        self._appdirs = AppDirs('homeslick')
        self.home_path = Path(os.environ['HOME'])
        self.castles_path = Path(self._appdirs.user_data_dir) / 'castles'
        self.config_path = Path(self._appdirs.user_config_dir) / 'config.yml'

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
