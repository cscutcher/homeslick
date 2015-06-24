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
def cli(home):
    '''Top level cli'''
    context = get_context()
