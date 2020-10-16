from django.contrib import admin

from .models import *
from mainapp.admin import HardDeleteAdmin

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ('item', 'quantity')
    fk_name = 'order'


class OrderAdmin(HardDeleteAdmin):
    fields = ('user', 'status', 'active')
    list_display = ('id', 'user', 'status', 'created', 'updated', 'active', 'deleted')
    inlines = (OrderItemInline,)


admin.site.register(Order, OrderAdmin)
