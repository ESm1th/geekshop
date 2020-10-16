from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models.signals import pre_save
from django.dispatch import receiver
# from django.utils.translation import ugettext_lazy as _
# from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import redirect

from .models import *

# Create your views here.


class BasketCreate(LoginRequiredMixin, CreateView):
    """Class for creating basket"""

    model = Basket
    fields = ('customer',)
    success_url = reverse_lazy('mainapp:main')

    def get(self, request, **kwargs):
        return self.post(request)

    def get_form_kwargs(self):
        return {'data': {'customer': self.request.user.id}}


class BasketUpdate(LoginRequiredMixin, UpdateView):
    """Class for updating basket object"""

    model = Basket
    fields = '__all__'
    success_url = reverse_lazy('mainapp:main')

    def get(self, request, **kwargs):
        return self.post(request)

    def get_object(self):
        if not self.request.user.get_card:
            BasketCreate.as_view()(self.request)
        return self.request.user.get_card

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = dict(kwargs['data'])
        kwargs['data'].update(
            {'customer': self.object.customer.id})
        return kwargs

    def form_valid(self, form):
        if not self.kwargs.get('pk') in self.object.basket_items.values_list('item_id', flat=True):
            return BasketItemCreate.as_view()(self.request, **self.kwargs)
        self.kwargs.update(
            {'pk': self.object.basket_items.get(item_id=self.kwargs.get('pk')).id})
        return BasketItemUpdate.as_view()(self.request, **self.kwargs)


class BasketItemCreate(LoginRequiredMixin, CreateView):
    """Class for creating basket item object"""

    model = BasketItem
    fields = ('card', 'item', 'quantity')

    def get(self, request, **kwargs):
        return self.post(request)

    def get_form_kwargs(self):
        kwargs = {
            'data': {
                'card': self.request.user.get_card.id,
                'item': self.kwargs.get('pk'),
                'quantity': self.kwargs.get('quantity')
            }
        }
        return kwargs


class BasketItemUpdate(LoginRequiredMixin, UpdateView):
    """Class for updating basket item quantity"""

    model = BasketItem
    fields = ('quantity',)

    def get(self, request, **kwargs):
        return self.post(request, **kwargs)

    def get_object(self):
        return self.model.objects.get(id=self.kwargs.get('pk'))

    def get_form_kwargs(self):
        if self.request.GET.get('quantity'):
            return {'data': {'quantity': self.request.GET.get('quantity')}}
        return {'data': {'quantity': self.kwargs.get('quantity')}}

    def form_valid(self, form):
        if self.request.is_ajax():
            self.object.quantity = form.cleaned_data.get('quantity')

            if self.object.quantity == 0:
                self.kwargs.update({'pk': self.object.id})
                BasketItemDelete.as_view()(self.request, **self.kwargs)
                values = self.request.user.get_card.get_summary
                data = {
                    'deleted': True,
                    'total_price': values.get('total_price'),
                    'total_items_quantity': values.get('total_items_quantity')
                }
            else:
                self.object.save()
                data = {
                    'value': self.object.quantity,
                    'price': self.object.price,
                    'total_price': self.request.user.get_card.get_summary.get('total_price')
                }
            return JsonResponse(data)

        self.object.quantity += form.cleaned_data.get('quantity')
        self.object.save()
        return redirect(self.model)


class BasketItemDelete(LoginRequiredMixin, DeleteView):
    """Class set basket_item 'Active' field to 'False' """

    model = BasketItem
    success_url = reverse_lazy('basketapp:basket_items')

    def get(self, request, **kwargs):
        return self.post(self.request, **kwargs)


class BasketItemList(LoginRequiredMixin, TemplateView):
    """Class shows list of basket items in template"""

    template_name = 'basketapp/basketitem_list.html'


@receiver(pre_save, sender=BasketItem)
def update_save_quantity(sender, update_fields, instance, **kwargs):
    if update_fields is 'quantity' or 'item':
        if instance.pk:
            instance.item.quantity -= instance.quantity - \
                instance._meta.model.objects.get(pk=instance.pk).quantity
        else:
            instance.item.quantity -= instance.quantity
        instance.item.save()
