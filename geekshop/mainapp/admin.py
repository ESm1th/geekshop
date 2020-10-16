from django.contrib import admin
from .models import *

# Register your models here.


class HardDeleteAdmin(admin.ModelAdmin):
    """Custom admin class for hard delete objects"""

    def get_queryset(self, request):
        return self.model.objects.get_all_queryset()

    def delete_model(self, request, instance):
        instance.hard_delete()

    def delete_queryset(self, request, queryset):
        queryset.hard_delete()


class CategoryAdmin(HardDeleteAdmin):
    fields = ('title', 'kind', 'active', 'sort', 'deleted')
    list_display = ('title', 'kind', 'active', 'sort', 'deleted')


admin.site.register(Category, CategoryAdmin)


class ManufacturerAdmin(HardDeleteAdmin):
    fields = ('title', 'active', 'sort', 'deleted')
    list_display = ('title', 'active', 'sort', 'deleted')


admin.site.register(Manufacturer, ManufacturerAdmin)


class ImageInline(admin.TabularInline):
    model = Image
    fk_name = 'product'
    fields = ('title', 'active', 'picture', 'deleted')


class ProductAdmin(HardDeleteAdmin):
    fields = ('title', 'category', 'creator',
              'price', 'quantity', 'gender', 'active', 'sort', 'deleted')
    list_display = ('title', 'category', 'creator',
                    'price', 'quantity', 'gender', 'active', 'sort', 'deleted')
    inlines = (ImageInline,)


admin.site.register(Product, ProductAdmin)
