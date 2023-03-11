from django.forms import ModelForm

from .models import Trade


class TradeForm(ModelForm):
    class Meta:
        model = Trade
        fields = ('operation', 'quantity')

        labels = {
            'operation': 'Операция',
            'quantity': 'Количество',
        }

        help_texts = {
            'operation': 'Покупка или продажа',
            'quantity': 'Желаемое количество',
        }
