# -*- coding: utf-8 -*-
"""
Castle definition
"""
import logging
import functools
from enum import Enum
from git import Repo
from homeslick import context
from homeslick.interfaces import ICastle
import zope.interface


DEV_LOGGER = logging.getLogger(__name__)


class CastleState(Enum):
    invalid = -1
    missing = 0
    outdated = 1
    fresh = 2
    dirty = 3


class InvalidCastleStateError(Exception):
    '''
    For when a function is called when the castle is in an invalid state
    '''


class _CastleStatusCheckWrapper(object):
    '''
    Decorator to wrap Castle methods to prevent them running when in invalid state
    '''
    def __init__(self, valid_states=None, invalid_states=None):
        self._valid_states = valid_states
        self._invalid_states = invalid_states

    def __call__(self, fn):
        '''
        Decorate fn
        '''
        @functools.wraps(fn)
        def wrapping_fn(castle, *args, **kwargs):
            status = castle.get_status()
            if self._valid_states is not None and (status not in self._valid_states):
                raise InvalidCastleStateError('{0} not in {1}'.format(status, self._valid_states))
            if self._invalid_states is not None and (status in self._invalid_states):
                raise InvalidCastleStateError('{0} in {1}'.format(status, self._valid_states))
            return fn(castle, *args, **kwargs)
        return wrapping_fn

castle_status_wrapper = _CastleStatusCheckWrapper


zope.interface.implementer(ICastle)
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
        self._branch = 'master'

    @property
    def log(self):
        return DEV_LOGGER.getChild(self.__class__.__name__).getChild(self._name)

    def get_status(self):
        '''
        Get status of castle
        '''
        status = self._get_status()
        self.log.info('Getting status: %s', status)
        return status

    def init(self):
        '''
        Initiliase castle
        '''
        return self._clone()

    @castle_status_wrapper(valid_states=(CastleState.outdated, CastleState.fresh))
    def pull(self):
        '''
        Update castle
        '''
        self._get_git_remote().pull(self._branch)

    def _get_status(self):
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

        if self._get_git_repo().is_dirty():
            return CastleState.dirty

        self._fetch()
        head_ref = self._get_git_repo().head.reference.object
        remote_ref = self._get_git_remote().refs[self._branch].object

        if head_ref == remote_ref:
            return CastleState.fresh
        else:
            return CastleState.outdated

    def _fetch(self):
        '''
        Do git fetch on castle
        '''
        self.log.info('Fetch')
        self._get_git_repo().remotes[self.REMOTE_NAME].fetch()

    @castle_status_wrapper(valid_states=(CastleState.missing,))
    def _clone(self):
        '''
        Do git clone on castle
        '''
        self.log.info('Clone')
        self._repo = Repo.clone_from(
            self._git_uri, str(self._staging_path), origin=self.REMOTE_NAME)

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

        self.log.debug('Initialise with repo: %r', repo)
        return repo

    def _get_git_remote(self):
        '''
        Get remote for castle
        '''
        return self._get_git_repo().remotes[self.REMOTE_NAME]

    def _get_git_repo(self):
        '''
        Get repo object for castle
        '''
        if self._repo is None:
            self._repo = self._initialise_git_repo()
        return self._repo
