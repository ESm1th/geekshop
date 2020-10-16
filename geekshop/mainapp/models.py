from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

# Create your models here.


class CoreQuerySet(models.QuerySet):
    """Custom queryset class, realization soft delete for QuerySet"""

    def delete(self):
        return super(CoreQuerySet, self).update(deleted=True, active=False)

    def hard_delete(self):
        return super(CoreQuerySet, self).delete()


class CoreManager(models.Manager):
    """Change initial QuerySet and queryset for superuser in admin panel"""

    def get_queryset(self):
        return CoreQuerySet(self.model).filter(active=True, deleted=False)

    def get_all_queryset(self):
        return CoreQuerySet(self.model)


class Core(models.Model):
    """Core abstract class"""

    title = models.CharField(_('title'), max_length=250, unique=True)
    description = models.TextField(_('description'), blank=True)
    sort = models.IntegerField(_('sort'), default=0, null=True, blank=True)
    active = models.BooleanField(_('active'), default=True)
    deleted = models.BooleanField(_('deleted'), default=False)

    objects = CoreManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    @property
    def verbose_name(self):
        return self._meta.verbose_name

    @property
    def verbose_name_plural(self):
        return self._meta.verbose_name_plural

    def delete(self):
        self.deleted = True
        self.save()

    def hard_delete(self):
        self.delete()


class Category(Core):
    """Class represent category table in db"""

    kind = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Manufacturer(Core):
    """Class represent manufacturer table in db"""

    class Meta:
        verbose_name = _('Manufacturer')
        verbose_name_plural = _('Manufacturers')


class Product(Core):
    """Class represent product table in db"""

    men = 'M'
    women = 'W'

    gender_choices = (
        (men, 'Men'),
        (women, 'Women'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    creator = models.ForeignKey(
        Manufacturer, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(
        _('Price'), max_digits=8, decimal_places=2, default=0, blank=True)
    quantity = models.PositiveIntegerField(
        _('Quantity on stock'), default=0, blank=True)
    gender = models.CharField(
        _('gender'), max_length=1, choices=gender_choices, default=men)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def get_absolute_url(self):
        return reverse_lazy('mainapp:detail', kwargs={'pk': self.id})


class Image(Core):
    """Class represent image table in db"""

    picture = models.ImageField(
        _('picture'), upload_to='media/images', max_length=250)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='pictures')

    class Meta:
        verbose_name = _('Picture')
        verbose_name_plural = _('Pictures')
