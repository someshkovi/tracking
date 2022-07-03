from typing import Any, Optional
from django.db.models import QuerySet, F
from django.contrib import admin
from products.models import Product, ProductCategory, ProductPriceChange, MultiProductCollectiveTracking
from django.utils.translation import gettext_lazy as _


class ProductListFilter(admin.SimpleListFilter):
    """
    https://docs.djangoproject.com/en/4.1/ref/contrib/admin/filters/
    """
    title = _('price filter')
    parameter_name = 'price_compare'

    def lookups(self, request, model_admin):
        return (
            ('lp', 'is at lowest price'),
            ('tp', 'reached target price'),
        )

    def queryset(self, request: Any, queryset: QuerySet) -> Optional[QuerySet]:
        if self.value() == 'lp':
            return queryset.filter(
                price__isnull=False).filter(min_price__isnull=False).filter(
                max_price__isnull=False).filter(min_price__lt=F('max_price'))
        if self.value() == 'tp':
            return queryset.filter(target_price__isnull=False).filter(target_price__gte=F('price'))


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'price', 'target_price', 'availability', 'user')
    ordering = ('site', 'name')
    list_filter = (ProductListFilter, 'availability', 'availability_message', 'is_url_valid')
    search_fields = ('url', 'name')
    fieldsets = [
        ('Info', {'fields': ['name', 'site', 'url', 'target_price']}),
        ('Price',
         {'fields': ['price', 'min_price', 'max_price'], 'classes':['collapse']}
         ),
        ('Rating and availability',
         {'fields': ['availability', 'availability_message', 'rating', 'reviews_count', 'ratings_count'],
          'classes': ['collapse']}),
    ]


admin.site.register(ProductCategory)
admin.site.register(ProductPriceChange)

admin.site.register(MultiProductCollectiveTracking)
