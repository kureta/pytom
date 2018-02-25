#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pytom.cli` module."""

from click.testing import CliRunner

from pytom import cli
from pytom.libs.bjorklund import bjorklund


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ['euclidean', '--steps-beats', 13, 5])
    assert result.exit_code == 0
    assert repr(bjorklund(13, 5)) + '\n' == result.output
    help_result = runner.invoke(cli.main, ['euclidean', '--help'])
    assert help_result.exit_code == 0
    assert '--steps-beats <int> <int>  Number of steps and number of pulses' in help_result.output
