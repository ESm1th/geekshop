from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, inlineformset_factory
from django import forms

from .models import *
from accounts.forms import ChangeWidgetMixin


class OrderForm(ChangeWidgetMixin, ModelForm):

    class Meta:
        model = Order
        exclude = ('user',)


class OrderItemForm(ChangeWidgetMixin, ModelForm):
    price = forms.CharField(label=_('price'), required=False)

    class Meta:
        model = OrderItem
        fields = ('item', 'quantity')


OrderFormset = inlineformset_factory(
    Order, OrderItem, form=OrderItemForm, can_delete=False, extra=1)
