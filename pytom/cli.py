# -*- coding: utf-8 -*-

"""Console script for pytom."""
import sys
import click

from pytom.libs.bjorklund import bjorklund


@click.command()
@click.option('--bjork', nargs=2, type=int, metavar='<int> <int>',
              prompt='Number of steps and number of pulses',
              help='Euclidean rhthym given a number of steps and a number of pulses to evenly distribute.')
def main(bjork):
    """Console script for pytom."""
    click.echo(repr(bjorklund(*bjork)))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
