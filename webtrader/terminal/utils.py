import base64
from io import BytesIO

from django.conf import settings
from matplotlib.figure import Figure


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
