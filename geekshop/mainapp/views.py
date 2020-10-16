# from django.shortcuts import render
# from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache

from .models import *
from .forms import *
from basketapp.views import BasketUpdate

# Create your views here.


class MainView(ListView):
    """Class process main page"""

    model = Product
    ordering = ['?']
    template_name = 'mainapp/index.html'

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related(
            'pictures').select_related('creator')
        return queryset


class ProductList(ListView):
    """Class process catalogue page"""

    model = Product
    paginated_by = 8
    columns = 2
    orphans = 0

    def get(self, request, **kwargs):
        response = super().get(request, **kwargs)

        if self.request.is_ajax():
            result = render_to_string(
                'mainapp/includes/inc_product_list.html',
                context=self.get_context_data(),
                request=self.request
            )
            return JsonResponse({'result': result})
        else:
            return response

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'creator', 'category').prefetch_related('pictures')
        if 'pk' in self.kwargs:
            queryset = queryset.filter(category=self.kwargs.get('pk'))
        return queryset

    def get_paginated_rows(self, dataset):
        paginator = self.paginator_class(dataset, self.columns, self.orphans)
        for page_num in paginator.page_range:
            yield paginator.page(page_num).object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            categories=self.get_categories(), **kwargs)
        context.update(
            {'obj_pages': [row for row in self.get_paginated_rows(self.object_list)]})
        return context

    def get_categories(self):
        if settings.LOW_CACHE:
            key = 'categories'
            categories = cache.get(key)
            if categories is None:
                categories = self.model.category.get_queryset()
                cache.set(key, categories)
            return categories
        else:
            return self.model.category.get_queryset()



class ProductDetail(FormView, DetailView):
    """Class process page with detail info about product"""

    model = Product
    form_class = AddBasketItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        similar = self.get_queryset().exclude(
            id=self.object.id).filter(category=self.object.category).order_by('?')
        context.update({'similar': similar})
        return context

    def form_valid(self, form):
        self.kwargs.update({'quantity': form.cleaned_data.get('quantity')})
        return BasketUpdate.as_view()(self.request, *self.args, **self.kwargs)
