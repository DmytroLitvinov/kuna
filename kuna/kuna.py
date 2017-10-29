# -*- coding: utf-8 -*-

"""Main module."""
import hashlib
import hmac
import json

import requests

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

API_VERSION = '2'
KUNA_API_URL_PREFIX = 'api/v{}'.format(API_VERSION)
KUNA_API_BASEURL = 'https://kuna.io/{}/'.format(KUNA_API_URL_PREFIX)

VALID_MARKET_DATA_PAIRS = ['btcuah', 'ethuah', 'wavesuah', 'gbguah', 'golosgbg', 'kunbtc', 'bchbtc']


class KunaAPI(object):
    def __init__(self, access_key=None, secret_key=None):

        self.access_key = access_key
        self.secret_key = secret_key

    def get_server_time(self):
        """
        Get the server time from server.
        :return: unix timestamp
        """
        return self.request('timestamp')

    def get_recent_market_data(self, market):
        """
        Get recent market data from server.
        :param market:
        :return:
        """
        if market not in VALID_MARKET_DATA_PAIRS:
            raise APIError('Enter a valid market pair')

        return self.request('{}/{}'.format('tickers', market))

    def get_order_book(self, market):
        """
        Get order book data from server.
        :param market:
        :return:
        """
        if market not in VALID_MARKET_DATA_PAIRS:
            raise APIError('Enter a valid market pair')

        args = {
            'market': market
        }
        return self.request('{}'.format('order_book'), args=args)

    def get_trades_history(self, market):
        """
        Get trades history data from server.
        :param market:
        :return:
        """
        if market not in VALID_MARKET_DATA_PAIRS:
            raise APIError('Enter a valid market pair')

        args = {
            'market': market
        }
        return self.request('{}'.format('trades'), args=args)

    def get_user_account_info(self):
        """
        Information about the User and Assets.
        This is a User method.
        :return:
        """
        return self.request('{}'.format('members/me'), is_user_method=True)

    def get_orders(self, market):
        """
        Active User Orders.
        This is a User method.
        :return:
        """
        if market not in VALID_MARKET_DATA_PAIRS:
            raise APIError('Enter a valid market pair')
        args = {
            'market': market
        }
        return self.request('{}'.format('orders'), args=args, is_user_method=True)

    def put_order(self, side, volume, market, price):
        """
        Order placing.
        This is a User method.
        :param side: 'buy' or 'sell'
        :param volume: volume in BTC
        :param market: option from VALID_MARKET_DATA_PAIRS
        :param price: price for 1 BTC
        :return:
        """
        if market not in VALID_MARKET_DATA_PAIRS:
            raise APIError('Enter a valid market pair')
        args = {
            'side': side,
            'volume': volume,
            'market': market,
            'price': price
        }
        return self.request('{}'.format('orders'), args=args, method='POST', is_user_method=True)

    def cancel_order(self, order_id):
        """
        Cancel order.
        This is a User method.
        :param order_id:
        :return:
        """
        args = {
            'id': order_id
        }
        return self.request('{}'.format('order/delete'), args=args, method='POST', is_user_method=True)

    def get_trade_history(self, market):
        """
        User trade history
        This is a User method.
        :param market:
        :return:
        """
        if market not in VALID_MARKET_DATA_PAIRS:
            raise APIError('Enter a valid market pair')

        args = {
            'market': market
        }
        return self.request('{}'.format('trades/my'), args=args, is_user_method=True)

    def request(self, path, args=None, method='GET', is_user_method=False):
        """
        Fetches the given path in the Kuna API.
        We translate args to a valid query string. If post_args is
        given, we send a POST request to the given path with the given
        arguments.
        :param path:
        :param args:
        :param method:
        :param is_user_method:
        :return:
        """
        if args is None:
            args = dict()

        if is_user_method:
            args_for_signature = [method, path, args]
            user_method_args = {
                'access_key': self.access_key,
                'tonce': self.get_server_time() * 1000,
                'signature': self._generate_signature(*args_for_signature)
            }
            args.update(user_method_args)

        try:
            response = requests.request(
                method,
                KUNA_API_BASEURL + path,
                params=args)
        except requests.RequestException as e:
            response = json.loads(e.read())
            raise APIError(response)

        result = response.json()

        if result and isinstance(result, dict) and result.get('error'):
            raise APIError(result)
        elif not response.status_code == requests.codes.ok:
            raise APIError(response.reason)
        return result

    def _generate_signature(self, method, path, args):
        """
        Signature is generated by an algorithm HEX(HMAC-SHA256("HTTP-verb|URI|params", secret_key))
        :param method:
        :param path:
        :param args:
        :return:
        """
        params = {
            'access_key': self.access_key,
            'tonce': self.get_server_time() * 1000
        }
        params.update(args)
        urlencoded_params = urlencode(params)

        uri = '/{}/{}'.format(KUNA_API_URL_PREFIX, path)
        msg = '{}|{}|{}'.format(method, uri, urlencoded_params)  # "HTTP-verb|URI|params"

        # HMAC can only handle ascii (byte) strings
        # https://bugs.python.org/issue5285
        key = self.secret_key.encode('ascii')
        msg = msg.encode('ascii')
        return hmac.new(key, msg, hashlib.sha256).hexdigest()


class APIError(Exception):
    def __init__(self, result):

        try:
            self.message = result["error"]["message"]
            self.code = result["error"].get("code")
        except:
            self.message = result

        Exception.__init__(self, self.message)
