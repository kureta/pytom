#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pytom.cli` module."""

from click.testing import CliRunner

from pytom import cli
from pytom.libs.bjorklund import bjorklund


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ['--bjork', 13, 5])
    assert result.exit_code == 0
    assert repr(bjorklund(13, 5)) + '\n' == result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--bjork <int> <int>  Euclidean rhthym given a number of steps and a number' in help_result.output
