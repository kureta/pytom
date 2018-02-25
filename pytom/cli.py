# -*- coding: utf-8 -*-

"""Console script for pytom.
Usage::

    $ pytom --bjorklund 8 3
    [3, 2, 3]

"""
import click

from pytom.libs.bjorklund import bjorklund


@click.group()
def main():
    pass


@click.command()
@click.option('--steps-beats', nargs=2, type=int, metavar='<int> <int>',
              help='Number of steps and number of pulses')
def euclidean(steps_beats):
    """Euclidean rhthym given a number of steps and a number of pulses to evenly distribute."""
    click.echo(repr(bjorklund(*steps_beats)))
    return 0


main.add_command(euclidean)
