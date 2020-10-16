from django.urls import path
from pathlib import PurePath
from .views import *
import os

app_name = PurePath(os.path.dirname(__file__)).parts[-1]

urlpatterns = [
    path('items/', BasketItemList.as_view(), name='basket_items'),
    path('items/edit/<int:pk>/',
         BasketItemUpdate.as_view(), name='edit'),
    path('items/delete/<int:pk>/',
         BasketItemDelete.as_view(), name='item_delete'),
]
