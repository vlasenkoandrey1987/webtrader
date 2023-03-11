from django.db import models


class Symbol(models.Model):
    ticker = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Тикер',
    )
    description = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Описание',
    )

    def __str__(self):
        return f'Symbol(t={self.ticker})'


class Tick(models.Model):
    symbol = models.ForeignKey(
        Symbol,
        on_delete=models.CASCADE,
        verbose_name='Инструмент',
    )
    price = models.FloatField(verbose_name='Цена')
    created = models.DateTimeField(
        verbose_name='Дата совершения сделки',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('created', )
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'

    def __str__(self):
        return f'Tick(s={self.symbol}, p={self.price})'
