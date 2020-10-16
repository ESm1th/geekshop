from django.views.decorators.cache import cache_page
from django.urls import path
import mainapp.views as mainapp
from pathlib import PurePath
import os

app_name = PurePath(os.path.dirname(__file__)).parts[-1]

urlpatterns = [
    path('', mainapp.MainView.as_view(), name='main'),
    path('products/', mainapp.ProductList.as_view(), name='products'),
    path('products/category/<int:pk>',
         cache_page(3600)(mainapp.ProductList.as_view()), name='products_category'),
    path('product/<int:pk>/', mainapp.ProductDetail.as_view(), name='detail'),
]
