import base64
from io import BytesIO

from django.conf import settings
from django.core.paginator import Paginator
from matplotlib.figure import Figure


def get_page(posts, page_number):
    paginator = Paginator(posts, settings.TRADES_PER_PAGE)
    return paginator.get_page(page_number)


def create_chart(ticks):
    width = settings.CHART_WIDTH
    height = settings.CHART_HEIGHT
    dpi = 120
    fig = Figure(figsize=(width / dpi, height / dpi), dpi=dpi)
    ax = fig.subplots()
    ax.plot(ticks)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    chart = base64.b64encode(buf.getbuffer()).decode("ascii")
    return chart
