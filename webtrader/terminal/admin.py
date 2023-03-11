from django.contrib import admin

from .models import Operation, Trade


class OperationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = '-пусто-'


admin.site.register(Operation, OperationAdmin)


class TradeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'symbol', 'operation', 'price', 'quantity', 'trader',
                    'created')
    list_editable = ('operation', )
    search_fields = ('symbol', 'operation')
    list_filter = ('symbol', 'operation', 'created', )
    empty_value_display = '-пусто-'


admin.site.register(Trade, TradeAdmin)
