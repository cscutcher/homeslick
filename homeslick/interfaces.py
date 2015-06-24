# -*- coding: utf-8 -*-
"""
Interfaces for homeslick
"""
import logging
import zope.interface

DEV_LOGGER = logging.getLogger(__name__)


class ICastle(zope.interface.Interface):
    '''
    All castle's implement ICastle
    '''
    def pull():
        '''
        Update castle from remote source and run any events that should be triggered after
        '''

    def push():
        '''
        Push local changes in castle up to remote source
        '''

    def init():
        '''
        Move Caste from missing state to fresh
        '''

    def get_status():
        '''
        Return state for Castle
        '''
