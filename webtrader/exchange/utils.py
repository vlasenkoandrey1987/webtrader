import random

from django.conf import settings
from exchange.models import Tick


def get_market_price(symbol):
    if not Tick.objects.filter(symbol=symbol).exists():
        return settings.START_PRICE

    tick = Tick.objects.filter(symbol=symbol).order_by('-created')[0]
    return tick.price


def calc_new_market_price(current_market_price):
    delta = random.randrange(-1, 2)
    return current_market_price + delta


def generate_new_tick(symbol):
    market_price = get_market_price(symbol)
    new_market_price = calc_new_market_price(market_price)
    Tick.objects.create(symbol=symbol, price=new_market_price)
