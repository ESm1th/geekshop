from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from mainapp.models import CoreQuerySet, CoreManager, Core, Product
from geekshop.settings import AUTH_USER_MODEL

# Create your models here.


class Basket(Core):
    """Class represent basket table in db"""

    customer = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    created = models.DateTimeField(_('created'), auto_now_add=True)
    title = None  # remove title field, because in Core class it is unique, and here this field not needed

    class Meta:
        verbose_name = _('Basket')
        verbose_name_plural = _('Baskets')

    def __str__(self):
        return 'id {}, created {}'.format(self.id, self.created)

    def delete(self):
        self.basket_items.delete()
        self.active = False
        self.save()
        super().delete()

    @cached_property
    def get_summary(self):
        items = self.get_items
        return {
            'total_price': sum([item.price for item in items]),
            'total_items_quantity': items.count()
        }

    @cached_property
    def get_items(self):
        return self.basket_items.select_related('item__creator', 'item').prefetch_related('item__pictures')


class BasketItemQueryset(CoreQuerySet):
    """Re-define 'delete' method"""

    def delete(self):
        for object in self:
            object.delete()
        super().delete()


class BasketItemManager(CoreManager):
    """
    Re-define 'get_queryset' method (assign new custom queryset) + define
    'delete' method, that call queryset's 'delete'
    """

    def get_queryset(self):
        return BasketItemQueryset(self.model).filter(active=True, deleted=False)

    def delete(self):
        return self.get_queryset().delete()


class BasketItem(Core):
    """Class represent basket_item table in db"""

    card = models.ForeignKey(
        Basket, related_name='basket_items', on_delete=models.CASCADE)
    item = models.ForeignKey(
        Product, related_name='item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    title = None

    objects = BasketItemManager()

    class Meta:
        verbose_name = _('Basket item')
        verbose_name_plural = _('Basket items')

    def __str__(self):
        return 'id {}, item - {}'.format(self.id, self.item)

    # def save(self, **kwargs):
    #     if self.pk:
    #         self.item.quantity -= self.quantity - \
    #             self._meta.model.objects.get(pk=self.pk).quantity
    #     else:
    #         self.item.quantity -= self.quantity
    #     self.item.save()
    #     super().save()

    def delete(self, **kwargs):
        self.item.quantity += self.quantity
        self.item.save()
        super().delete()

    @staticmethod
    def get_absolute_url():
        return reverse_lazy('basketapp:basket_items')

    @staticmethod
    def get_user_card(user):
        return BasketItem.card.field.related_model.objects.get_basket(user)

    @property
    def price(self):
        return self.item.price * self.quantity
