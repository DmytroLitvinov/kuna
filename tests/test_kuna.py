#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings
import unittest
from click.testing import CliRunner

from kuna import cli
from kuna.kuna import KunaAPI

warnings.filterwarnings("ignore")

try:
    from secret import public_key, private_key
except:
    public_key, private_key = None, None


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
        assert "kuna.cli.main" in result.output
        help_result = runner.invoke(cli.main, ["--help"])
        assert help_result.exit_code == 0
        assert "--help  Show this message and exit." in help_result.output

    def test_get_server_time(self):
        self.api.get_server_time()

    def test_get_order_book(self):
        self.api.get_order_book("btcuah")

    def test_get_trades_history(self):
        self.api.get_trades_history("btcuah")

    @unittest.skipIf(
        (private_key is None) or (public_key is None), "Methods need authentication"
    )
    def test_get_user_account_info(self):
        self.api.get_user_account_info()


class TestPublicAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = KunaAPI(public_key, private_key)

    def test_timestamp(self):
        resp = self.api.timestamp()
        self.assertIsInstance(resp, dict)

    def test_landing_page_statistic(self):
        resp = self.api.landing_page_statistic()
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

    def test_trades_hist(self):
        resp = self.api.trades_hist("btcuah")
        self.assertIsInstance(resp, list)

    def test_tickers(self):
        resp = self.api.tickers()
        self.assertIsInstance(resp, list)

    def test_book(self):
        resp = self.api.book("btcuah")
        self.assertIsInstance(resp, list)

    def test_fees(self):
        resp = self.api.fees()
        self.assertIsInstance(resp, list)


@unittest.skipIf(
    (private_key is None) or (public_key is None), "Methods need authentication"
)
class TestPrivateAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = KunaAPI(public_key, private_key)

    def test_http_test(self):
        resp = self.api.http_test()
        self.assertIsInstance(resp, dict)

    def test_auth_me(self):
        resp = self.api.auth_me()
        self.assertIsInstance(resp, dict)

    def test_auth_r_wallets(self):
        resp = self.api.auth_r_wallets()
        self.assertIsInstance(resp, list)

    @unittest.expectedFailure
    def test_auth_history_trades(self):
        resp = self.api.auth_history_trades("ethuah")
        self.assertIsInstance(resp, dict)


@unittest.skipIf(private_key is None, "Methods need authentication")
class TestTradeAPI(unittest.TestCase):
    order_id = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.api = KunaAPI(public_key, private_key)

    def test_auth_r_orders(self):
        resp = self.api.auth_r_orders()
        self.assertIsInstance(resp, list)

    def test_auth_r_orders_hist(self):
        resp = self.api.auth_r_orders_hist()
        self.assertIsInstance(resp, list)

    @unittest.expectedFailure
    def test_auth_r_order_trades(self):
        resp = self.api.auth_r_order_trades("ethuah", 1)
        self.assertIsInstance(resp, list)

    def test_4_auth_w_order_submit(self):
        resp = self.api.auth_w_order_submit("ethuah", "limit", amount=1.0, price=1.0)
        self.__class__.order_id = resp[0]
        self.assertIsInstance(resp, list)

    def test_5_order_cancel(self):
        resp = self.api.order_cancel(self.__class__.order_id)
        self.assertIsInstance(resp, dict)

    def test_6_order_cancel_multi(self):
        resp = self.api.order_cancel_multi(order_ids=[self.order_id])
        self.assertIsInstance(resp, dict)


@unittest.skipIf(private_key is None, "Methods need authentication")
class TestMerchantAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = KunaAPI(public_key, private_key)

    def test_deposit_channels(self):
        resp = self.api.deposit_channels("uah")
        self.assertIsInstance(resp, list)

    def test_withdraw_channels(self):
        resp = self.api.withdraw_channels("uah")
        self.assertIsInstance(resp, list)

    @unittest.expectedFailure
    def test_auth_payment_requests_address(self):
        resp = self.api.auth_payment_requests_address("ethuah")
        self.assertIsInstance(resp, dict)

    def test_auth_deposit_info(self):
        resp = self.api.auth_deposit_info("uah")
        self.assertIsInstance(resp, dict)

    @unittest.expectedFailure
    def test_auth_deposit(self):
        resp = self.api.auth_deposit(
            currency="uah", amount=1, payment_service="default", deposit_from=""
        )
        self.assertIsInstance(resp, dict)

    @unittest.expectedFailure
    def test_auth_deposit_details(self):
        resp = self.api.auth_deposit_details(1)
        self.assertIsInstance(resp, dict)

    def test_auth_withdraw_prerequest(self):
        resp = self.api.auth_withdraw_prerequest("uah")
        self.assertIsInstance(resp, dict)

    @unittest.expectedFailure
    def test_auth_withdraw(self):
        resp = self.api.auth_withdraw("uah", 1.0)
        self.assertIsInstance(resp, dict)

    @unittest.expectedFailure
    def test_auth_withdraw_details(self):
        resp = self.api.auth_withdraw_details(1)
        self.assertIsInstance(resp, dict)

    def test_assets_history(self):
        resp = self.api.assets_history()
        self.assertIsInstance(resp, dict)

    @unittest.expectedFailure
    def test_auth_merchant_deposit(self):
        resp = self.api.auth_merchant_deposit("uah", 1.0)
        self.assertIsInstance(resp, dict)

    @unittest.expectedFailure
    def test_auth_merchant_payment_services(self):
        resp = self.api.auth_merchant_payment_services("uah")
        self.assertIsInstance(resp, dict)


@unittest.skipIf(private_key is None, "Methods need authentication")
class TestKunaCodesAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = KunaAPI(public_key, private_key)

    def test_kuna_codes_check(self):
        resp = self.api.kuna_codes_check("857ny")
        self.assertIsInstance(resp, dict)

    @unittest.expectedFailure
    def test_kuna_codes(self):
        resp = self.api.kuna_codes("uah", 0.5)
        self.assertIsInstance(resp, dict)

    @unittest.expectedFailure
    def test_auth_kuna_codes_details(self):
        resp = self.api.auth_kuna_codes_details(1)
        self.assertIsInstance(resp, dict)

    @unittest.expectedFailure
    def test_auth_kuna_codes_redeem(self):
        resp = self.api.auth_kuna_codes_redeem(
            "857ny-XXXXX-XXXXX-XXXXX-XXXXX-XXXXX-XXXXX-XXXXX-XXXXX-KUN-KCode"
        )
        self.assertIsInstance(resp, dict)

    def test_auth_kuna_codes_issued_by_me(self):
        resp = self.api.auth_kuna_codes_issued_by_me()
        self.assertIsInstance(resp, dict)

    def test_auth_kuna_codes_redeemed_by_me(self):
        resp = self.api.auth_kuna_codes_redeemed_by_me()
        self.assertIsInstance(resp, dict)


if __name__ == "__main__":
    unittest.main()
