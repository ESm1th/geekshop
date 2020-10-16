from django.contrib import admin

from .models import *
from mainapp.admin import HardDeleteAdmin

# Register your models here.


class BasketAdmin(HardDeleteAdmin):
    fields = ('customer', 'active')
    list_display = ('id', 'customer', 'created', 'active')


admin.site.register(Basket, BasketAdmin)


class BasketItemAdmin(HardDeleteAdmin):
    fields = ('card', 'item', 'quantity')
    list_display = ('id', 'card', 'item', 'quantity')


admin.site.register(BasketItem, BasketItemAdmin)
