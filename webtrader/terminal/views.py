from django.conf import settings
from django.shortcuts import render
from exchange.models import Symbol, Tick

from .utils import create_chart


def _get_last_prices(symbol, count):
    ticks = Tick.objects.filter(symbol=symbol).order_by('-created')[0:count]
    prices = [tick.price for tick in reversed(ticks)]
    return prices


def index(request):
    template = 'terminal/index.html'

    ticker = settings.TICKER
    symbol = Symbol.objects.get(ticker=ticker)
    tick_count = settings.CHART_TICK_COUNT
    prices = _get_last_prices(symbol, tick_count)
    chart = create_chart(prices)
    context = {'symbol': symbol, 'chart': chart}

    return render(request, template, context)
