#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from click.testing import CliRunner

from kuna import cli
from kuna.kuna import KunaAPI

try:
    from secret import public_key, private_key
except:
    print("No key were found. Put variables 'public_key' and 'private_key' into secrets.py")
    public_key, private_key = None, None
else:
    print("Public and Private keys are successfully imported")


class TestKuna(unittest.TestCase):
    """Tests for `kuna` package."""
    @classmethod
    def setUpClass(cls) -> None:
        """Set up test fixtures, if any."""
        cls.api = KunaAPI(public_key, private_key)

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

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
        self.api.get_server_time()

    def test_get_order_book(self):
        self.api.get_order_book('btcuah')

    @unittest.expectedFailure
    def test_get_trades_history(self):
        self.api.get_trades_history('btcuah')

    def test_get_user_account_info(self):
        self.api.get_user_account_info()


class TestPublicAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Set up test fixtures, if any."""
        cls.api = KunaAPI(public_key, private_key)

    def test_timestamp(self):
        resp = self.api.timestamp()
        self.assertIsInstance(resp, dict)

    def test_currencies(self):
        resp = self.api.currencies()
        self.assertIsInstance(resp, list)

    def test_exchange_rates(self):
        resp = self.api.exchange_rates()
        self.assertIsInstance(resp, list)

    def test_markets(self):
        resp = self.api.markets()
        self.assertIsInstance(resp, list)

    def test_tickers(self):
        resp = self.api.tickers()
        self.assertIsInstance(resp, list)

    def test_book(self):
        resp = self.api.book('btcuah')
        self.assertIsInstance(resp, list)

    def test_fees(self):
        resp = self.api.fees()
        self.assertIsInstance(resp, list)


@unittest.skipIf(private_key is None, "Methods need authentication")
class TestPrivateAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Set up test fixtures, if any."""
        cls.api = KunaAPI(public_key, private_key)

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass


@unittest.skipIf(private_key is None, "Methods need authentication")
class TestTradeAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Set up test fixtures, if any."""
        cls.api = KunaAPI(public_key, private_key)

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass


@unittest.skipIf(private_key is None, "Methods need authentication")
class TestMerchantAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Set up test fixtures, if any."""
        cls.api = KunaAPI(public_key, private_key)

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

@unittest.skip
@unittest.skipIf(private_key is None, "Methods need authentication")
class TestKunaCodesAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Set up test fixtures, if any."""
        cls.api = KunaAPI(public_key, private_key)

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_kuna_codes_check(self):
        resp = self.api.kuna_codes_check('857ny')
        self.assertIsInstance(resp, dict)

    @unittest.expectedFailure
    def test_kuna_codes(self):
        resp = self.api.kuna_codes('uah', 0.5)
        self.assertIsInstance(resp, dict)

    @unittest.expectedFailure
    def test_auth_kuna_codes_details(self):
        resp = self.api.auth_kuna_codes_details(1)
        self.assertIsInstance(resp, dict)

    @unittest.expectedFailure
    def test_auth_kuna_codes_redeem(self):
        resp = self.api.auth_kuna_codes_redeem('857ny-XXXXX-XXXXX-XXXXX-XXXXX-XXXXX-XXXXX-XXXXX-XXXXX-KUN-KCode')
        self.assertIsInstance(resp, dict)

    def test_auth_kuna_codes_issued_by_me(self):
        resp = self.api.auth_kuna_codes_issued_by_me()
        self.assertIsInstance(resp, dict)

    def test_auth_kuna_codes_redeemed_by_me(self):
        resp = self.api.auth_kuna_codes_redeemed_by_me()
        self.assertIsInstance(resp, dict)

if __name__ == '__main__':
    unittest.main()

