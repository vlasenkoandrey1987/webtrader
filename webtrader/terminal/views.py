from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import ExpressionWrapper, F, FloatField, Sum
from django.shortcuts import redirect, render
from exchange.models import Symbol, Tick
from exchange.utils import get_market_price

from .forms import TradeForm
from .models import Trade
from .utils import create_chart, get_logger, get_page


def _get_last_prices(symbol, count):
    ticks = Tick.objects.filter(symbol=symbol).order_by('-created')[0:count]
    prices = [tick.price for tick in reversed(ticks)]
    return prices


def _get_trade_page(symbol, trader, page_number):
    with get_logger('django.db.backends') as logger:
        trades = Trade.objects.select_related(
            'symbol',
            'operation',
            'trader',
        ).filter(
            symbol=symbol,
            trader=trader,
        )
        logger.debug(trades)
    return get_page(trades, page_number)


def _get_balance(symbol, trader):
    balance = Trade.objects.select_related(
        'symbol',
        'trader',
    ).filter(
        symbol=symbol,
        trader=trader,
    ).values('operation__name').annotate(
        operation=F('operation__name'),
    ).annotate(
        total=Sum(F('price') * F('quantity'), output_field=FloatField()),
        quantity=Sum('quantity'),
    ).annotate(
        average_price=ExpressionWrapper(
            F('total') / F('quantity'), output_field=FloatField(),
        ),
    ).order_by()
    return balance


@login_required
def index(request):
    template = 'terminal/index.html'

    ticker = settings.TICKER
    symbol = Symbol.objects.get(ticker=ticker)

    form = TradeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        trade = form.save(commit=False)
        trade.symbol = symbol
        trade.price = get_market_price(symbol)
        trade.trader = request.user
        trade.save()
        return redirect('terminal:index')

    prices = _get_last_prices(symbol, settings.CHART_TICK_COUNT)
    chart = create_chart(prices)

    page = _get_trade_page(symbol, request.user, request.GET.get('page', 1))

    balance = _get_balance(symbol, request.user)

    context = {
        'symbol': symbol,
        'form': form,
        'chart': chart,
        'trades': page,
        'balance': balance,
    }
    return render(request, template, context)
