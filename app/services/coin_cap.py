from configuration.configuration import Configuration
from datetime import datetime, timedelta
from helper.request import http_request
from models.currency import CurrencyModel

AVAILABLE_CURRENCIES_CODES = dict()
VALUE_CACHE = {"values": dict(), "last_update": datetime.min}


class CoinCapService:
    def __init__(self):
        self._coin_cap_base_url = Configuration().coin_cap_url

    def converter(self, crypto_currency: CurrencyModel, amount: float):
        self._load_cache()
        value = VALUE_CACHE["values"][crypto_currency.code]
        return amount * value

    def _load_cache(self):
        last_update = datetime.utcnow() - VALUE_CACHE["last_update"]

        if last_update < timedelta(seconds=Configuration().cache_timeout):
            return

        response = http_request(self._coin_cap_base_url, "assets/")
        currencies = response.json()["data"]

        VALUE_CACHE["values"] = {
            c["symbol"]: float(c["priceUsd"]) for c in currencies
        }
        VALUE_CACHE["last_update"] = datetime.utcnow()

    def is_currency_available(self, currency):
        self._build_available_currencies()
        for code in AVAILABLE_CURRENCIES_CODES.keys():
            if code == currency.code:
                return True

        return False

    def _build_available_currencies(self):
        if AVAILABLE_CURRENCIES_CODES:
            return

        response = http_request(self._coin_cap_base_url, "assets/")
        currencies = response.json()["data"]
        currencies_from_api = {
            c["symbol"]: c["name"].lower() for c in currencies
        }
        AVAILABLE_CURRENCIES_CODES.update(currencies_from_api)
