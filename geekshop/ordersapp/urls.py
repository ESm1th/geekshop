from django.urls import path
from pathlib import PurePath
from .views import *
import os

app_name = PurePath(os.path.dirname(__file__)).parts[-1]

urlpatterns = [
    path('list/', OrderList.as_view(), name='list'),
    path('create/', OrderItemsCreate.as_view(), name='create'),
    path('update/<int:pk>/', OrderStatusUpdate.as_view(), name='status_update'),
    path('update/<int:pk>/items/', OrderItemsUpdate.as_view(), name='items_update'),
    path('item/get/price/<int:pk>/', FetchOrderItemPrice.as_view(), name='get_price'),
    path('detail/<int:pk>/', OrderDetail.as_view(), name='detail'),
    path('delete/order/<int:pk>/', OrderDelete.as_view(), name='delete'),
    path('delete/item/<int:pk>/', OrderItemDelete.as_view(), name='item_delete'),
]
