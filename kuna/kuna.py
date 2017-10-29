# -*- coding: utf-8 -*-

"""Main module."""
import json

import requests

API_VERSION = '2'
KUNA_API_BASEURL = 'https://kuna.io/api/v{}/'.format(API_VERSION)

VALID_MARKET_DATA_PAIRS = ['btcuah', 'ethuah', 'wavesuah', 'gbguah', 'golosgbg', 'kunbtc', 'bchbtc']


class KunaAPI(object):
    def __init__(self, access_token=None):

        self.access_token = access_token

    def get_server_time(self):
        """
        Get the server time from server.
        :return: unix timestamp
        """
        return self.request('timestamp')

    def get_recent_market_data(self, pair):
        """
        Get recent market data from server.
        :param pair:
        :return:
        """
        if pair not in VALID_MARKET_DATA_PAIRS:
            raise APIError('Enter a valid pair')
        return self.request('{}/{}'.format('tickers', pair))

    def get_order_book(self, pair):
        """
        Get order book data from server.
        :param pair:
        :return:
        """
        if pair not in VALID_MARKET_DATA_PAIRS:
            raise APIError('Enter a valid pair')

        args = {
            'market': pair
        }
        return self.request('{}'.format('order_book'), args=args)

    def get_trades_history(self, pair):
        """
        Get trades history data from server.
        :param pair:
        :return:
        """
        if pair not in VALID_MARKET_DATA_PAIRS:
            raise APIError('Enter a valid pair')

        args = {
            'market': pair
        }
        return self.request('{}'.format('trades'), args=args)

    def request(self, path, args=None, post_args=None, method='GET'):
        """
        Fetches the given path in the Kuna API.
        We translate args to a valid query string. If post_args is
        given, we send a POST request to the given path with the given
        arguments.
        :param path:
        :param args:
        :param post_args:
        :param method:
        :return:
        """
        if args is None:
            args = dict()
        if post_args is not None:
            method = 'POST'

        try:
            response = requests.request(
                method,
                KUNA_API_BASEURL + path,
                params=args,
                data=post_args)
        except requests.RequestException as e:
            response = json.loads(e.read())
            raise APIError(response)

        result = response.json()

        if result and isinstance(result, dict) and result.get('error'):
            raise APIError(result)
        elif not response.status_code == requests.codes.ok:
            raise APIError(response.reason)
        return result


class APIError(Exception):
    def __init__(self, result):

        try:
            self.message = result["error"]["message"]
            self.code = result["error"].get("code")
        except:
            try:
                self.message = result["error_msg"]
            except:
                self.message = result

        Exception.__init__(self, self.message)
