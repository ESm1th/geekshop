from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import DetailView, View
from django.views.generic.detail import SingleObjectMixin
from django.db import transaction
# from django.utils.translation import ugettext_lazy as _
# from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
# from django.shortcuts import redirect
from .models import *
from .forms import *

# Create your views here.


class OrderList(LoginRequiredMixin, ListView):
    """Class lists all orders in template"""

    model = Order

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class OrderDetail(LoginRequiredMixin, DetailView):
    """Renders detail info of significant order"""

    model = Order

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('order_items__item')
        print(queryset.query)
        return queryset


class OrderStatusUpdate(LoginRequiredMixin, UpdateView):
    """Updates status when click on 'buy' in '_detail' template"""

    model = Order
    fields = ('status',)

    def get(self, request, **kwargs):
        return self.post(request, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'data': {'status': self.object.SENT_TO_PROCEED}})
        return kwargs


class OrderDelete(LoginRequiredMixin, DeleteView):
    """Class for deleting order"""

    model = Order
    success_url = reverse_lazy('ordersapp:list')

    def get(self, request, **kwargs):
        return self.post(request, **kwargs)


class OrderItemsFormsetMixin():
    """Mixin sets same attributes for classes"""

    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')

    def dispatch(self, request, **kwargs):

        if self.kwargs.get('pk'):
            obj = self.get_object()
            self.items = obj.order_items
            instance = obj
        else:
            self.items = self.request.user.get_card.get_items
            instance = None

        if self.request.method == 'POST':
            self.formset = OrderFormset(self.request.POST, instance=instance)
        else:
            self.formset = OrderFormset(instance=instance)

        return super().dispatch(request, **kwargs)


class OrderItemsCreate(LoginRequiredMixin, OrderItemsFormsetMixin, CreateView):
    """Class for creating order with items"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.method == 'POST':
            if self.items:
                self.formset.extra = self.items.count()
                for num, form in enumerate(self.formset.forms):
                    form.initial = {
                        'item': self.items.all()[num].item,
                        'quantity': self.items.all()[num].quantity,
                        'price': self.items.all()[num].price
                    }

        context.update({'formset': self.formset})
        return context

    def form_valid(self, form):
        formset = self.formset

        with transaction.atomic():
            form.instance.user = self.request.user
            response = super().form_valid(form)

            if formset.is_valid():
                formset.instance = self.object
                formset.save()

            self.items._hints.get('instance').delete()
            if not self.object.total_items_quantity:
                self.object.delete()
            return response


class OrderItemsUpdate(LoginRequiredMixin, OrderItemsFormsetMixin, UpdateView):
    """Update order items in order"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # receive ids for all products in order and set queryset for extra formset's item field
        ids = Product.objects.exclude(
            id__in=self.object.order_items.values_list('item_id', flat=True))
        self.formset.forms[-1].fields['item'].queryset = ids

        for form in self.formset.forms:
            if form.instance.pk:
                form.initial['price'] = form.instance.item.price

        context.update({'formset': self.formset})
        return context

    def form_valid(self, form):
        formset = self.formset

        with transaction.atomic():
            response = super().form_valid(form)

            if formset.is_valid():
                formset.save()

            if not self.object.total_items_quantity:
                self.object.delete()

            return response


class FetchOrderItemPrice(LoginRequiredMixin, SingleObjectMixin, View):
    """Class that fetch price of order item's product with ajax request"""

    model = Product

    def get(self, request, **kwargs):
        if self.request.is_ajax():
            data = {'price': self.get_object().price}
            return JsonResponse(data)


class OrderItemDelete(LoginRequiredMixin, DeleteView):
    """Class for deleting order item"""

    model = OrderItem
    success_url = reverse_lazy('ordersapp:list')

    def get(self, request, **kwargs):
        return self.post(request, **kwargs)

    def post(self, request, **kwargs):
        order = self.get_object().order
        response = super().post(request, **kwargs)
        if not order.order_items.all():
            order.delete()
        return response
