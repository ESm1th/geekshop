from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mainapp.models import CoreManager, CoreQuerySet, Core, Product
from geekshop.settings import AUTH_USER_MODEL

# Create your models here.


class Order(Core):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, _('forming')),
        (SENT_TO_PROCEED, _('send to proceed')),
        (PAID, _('paid')),
        (PROCEEDED, _('proceeded')),
        (READY, _('ready')),
        (CANCEL, _('cancel')),
    )

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    status = models.CharField(_('status'), max_length=3,
                              choices=ORDER_STATUS_CHOICES, default=FORMING)
    title = None

    class Meta:
        ordering = ('-created',)
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return 'Order {}, created {}'.format(self.id, self.created)

    def get_absolute_url(self):
        return reverse_lazy('ordersapp:list')

    def delete(self):
        self.order_items.delete()
        self.active = False
        self.save()
        super().delete()

    @property
    def total_items_quantity(self):
        return self.order_items.count()

    @property
    def total_quantity(self):
        return sum([item.quantity for item in self.order_items.all()])

    @property
    def total_price(self):
        return sum([item.price for item in self.order_items.all()])


class OrderItemQueryset(CoreQuerySet):
    """Re-define 'delete' method"""

    def delete(self):
        for object in self:
            object.delete()
        super().delete()


class OrderItemManager(CoreManager):
    """
    Re-define 'get_queryset' method (assign new custom queryset) + define
    'delete' method, that call queryset's 'delete'
    """

    def get_queryset(self):
        return OrderItemQueryset(self.model).filter(active=True, deleted=False)

    def delete(self):
        return self.get_queryset().delete()


class OrderItem(Core):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE)
    item = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_('quantity'), default=0)
    title = None

    objects = OrderItemManager()

    def __str__(self):
        return 'id {}, item - {}'.format(self.id, self.item)

    def save(self, **kwargs):
        if self.pk:
            self.item.quantity -= self.quantity - \
                self._meta.model.objects.get(pk=self.pk).quantity
        else:
            self.item.quantity -= self.quantity
        self.item.save()
        super().save()

    def delete(self):
        self.item.quantity += self.quantity
        self.item.save()
        super().delete()

    @property
    def price(self):
        return self.item.price * self.quantity
