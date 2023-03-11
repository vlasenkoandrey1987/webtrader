from django.contrib.auth import get_user_model
from django.db import models
from exchange.models import Symbol

User = get_user_model()


class Operation(models.Model):
    name = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Название',
    )

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'

    def __str__(self):
        return self.name


class Trade(models.Model):
    symbol = models.ForeignKey(
        Symbol,
        on_delete=models.CASCADE,
        verbose_name='Инструмент',
    )
    operation = models.ForeignKey(
        Operation,
        on_delete=models.CASCADE,
        verbose_name='Операция',
    )
    price = models.FloatField(verbose_name='Цена')
    quantity = models.IntegerField(verbose_name='Количество')
    trader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='trades',
        verbose_name='Трейдер',
    )
    created = models.DateTimeField(
        verbose_name='Дата совершения сделки',
        auto_now_add=True,
    )

    @property
    def total(self):
        return self.price * self.quantity

    class Meta:
        ordering = ('-created', )
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'

    def __str__(self):
        return (f'Trade('
                f'op={self.operation}, p={self.price}, q={self.quantity}, '
                f't={self.trader}'
                f')')
