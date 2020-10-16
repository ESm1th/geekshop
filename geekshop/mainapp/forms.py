from django import forms
from accounts.forms import ChangeWidgetMixin


class AddBasketItemForm(ChangeWidgetMixin, forms.Form):
    quantity = forms.IntegerField(initial=1, min_value=1, max_value=20)
