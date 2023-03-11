from django.conf import settings
from exchange.models import Symbol
from exchange.utils import generate_new_tick


def exchange_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        ticker = settings.TICKER
        symbol = Symbol.objects.get(ticker=ticker)
        generate_new_tick(symbol)

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
