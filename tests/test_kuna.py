#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `kuna` package."""


import unittest
from click.testing import CliRunner

from kuna import cli


class TestKuna(unittest.TestCase):
    """Tests for `kuna` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'kuna.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    def test_get_server_time(self):
        pass

    def test_get_recent_market_data(self):
        pass

    def test_get_order_book(self):
        pass

    def test_get_trades_history(self):
        pass
