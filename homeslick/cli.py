# -*- coding: utf-8 -*-
"""
Homeslick CLI
"""
import logging
import click
from homeslick.context import get_context

DEV_LOGGER = logging.getLogger(__name__)


@click.group()
@click.option(
    '--home',
    default=None,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True),
    help='Set homeslick to use a different path as home')
@click.option(
    '--debug/--no-debug',
    default=False,
    help='Debug logging')
def cli(home, debug):
    '''Top level cli'''
    context = get_context()

    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    DEV_LOGGER.info('%r', context)


@cli.command()
def init():
    '''
    Do init
    '''


@cli.command()
def pull():
    '''
    Do pull
    '''
