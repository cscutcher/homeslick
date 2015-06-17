# -*- coding: utf-8 -*-
"""
Castle definition
"""
import logging
from enum import Enum
from git import Repo
from homeslick import context


DEV_LOGGER = logging.getLogger(__name__)


class CastleState(Enum):
    invalid = -1
    missing = 0
    outdated = 1
    fresh = 2


class Castle(object):
    '''
    The castle object stores a single component of a home environment
    which is backed on a git repository cloned from one or more environments.

    These environments are checked out into the homeslick staging area.
    '''
    REMOTE_NAME = 'homeslick_origin'

    def __init__(self, name, git_uri):
        self._name = name
        self._git_uri = git_uri
        self._global_context = context.get_context()
        self._staging_path = self._global_context.castles_path / self._name
        self._staging_git_path = self._staging_path / '.git'
        self._repo = None

    @property
    def log(self):
        return DEV_LOGGER.getChild(self.__class__.__name__).getChild(self._name)

    def get_status(self):
        '''
        Get status of castle
        '''
        if not self._staging_path.exists():
            return CastleState.missing

        if not self._staging_path.is_dir():
            self.log.error('Castle exists but is not directory')
            return CastleState.invalid

        if not self._staging_git_path.is_dir():
            self.log.error('Castle exists but it\'s git directory is missing or invalid')
            return Castle.invalid

    def fetch(self):
        '''
        Do git fetch on castle
        '''
        self.get_git_repo().remotes.origin.fetch()

    def _initialise_git_repo(self):
        '''
        Get a fresh initialised Repo object
        '''
        repo = Repo(str(self._staging_git_path))
        main_remote = repo.remotes[self.REMOTE_NAME]

        if main_remote.exists():
            config_writer = main_remote.config_writer
            config_writer.set('url', self._git_uri)
            config_writer.release()
        else:
            repo.create_remote(self.REMOTE_NAME, self._git_uri)
        return repo

    def get_git_remote(self):
        '''
        Get remote for castle
        '''
        return self.get_git_repo().remotes[self.REMOTE_NAME]

    def get_git_repo(self):
        '''
        Get repo object for castle
        '''
        if self._repo is None:
            self._repo = self._initialise_git_repo()
        return self._repo
