from typing import Any, Optional
from django.db.models import QuerySet, F
from django.contrib import admin
from products.models import Product, ProductCategory, ProductPriceChange, MultiProductCollectiveTracking
from django.utils.translation import gettext_lazy as _
from datetime import timedelta, datetime

class ProductListFilter(admin.SimpleListFilter):
    """
    https://docs.djangoproject.com/en/4.1/ref/contrib/admin/filters/
    """
    title = _('custom filters')
    parameter_name = 'custom_filters'

    def lookups(self, request, model_admin):
        return (
            ('lp', 'is at lowest price'),
            ('tp', 'reached target price'),
            ('up_24', 'updated in last 24 hours'),
            ('not_up_24', 'not updated in last 24 hours'),
            ('not_up_1', 'not updated in last 1 hour')
        )

    def queryset(self, request: Any, queryset: QuerySet) -> Optional[QuerySet]:
        if self.value() == 'lp':
            return queryset.filter(
                price__isnull=False).filter(min_price__isnull=False).filter(
                max_price__isnull=False).filter(min_price__lt=F('max_price'))
        if self.value() == 'tp':
            return queryset.filter(target_price__isnull=False).filter(target_price__gte=F('price'))

        if self.value() == 'up_24':
            return queryset.filter(updated__gt=datetime.now()-timedelta(days=1))

        if self.value() == 'not_up_24':
            return queryset.filter(updated__lt=datetime.now()-timedelta(days=1))

        if self.value() == 'not_up_1':
            return queryset.filter(updated__lt=datetime.now()-timedelta(hours=1))


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'price', 'target_price', 'availability', 'user', 'rating')
    ordering = ('site', 'name')
    list_filter = (ProductListFilter, 'availability', 'availability_message', 'is_url_valid', 'only_for_search')
    search_fields = ('url', 'name')
    readonly_fields=('created', 'updated', 'user', 'is_url_valid', 'name_in_site')
    fieldsets = [
        ('Info', {'fields': ['name', 'site', 'url', 'target_price', 'only_for_search']}),
        ('Price',
         {'fields': ['price', 'min_price', 'max_price'], 'classes':['collapse']}
         ),
        ('Rating and availability',
         {'fields': ['availability', 'availability_message', 'rating', 'reviews_count', 'ratings_count'],
          'classes': ['collapse']}),
        ('Read only',
        {'fields': ['created', 'updated', 'user', 'is_url_valid', 'name_in_site'],
        'classes':['collapse']})
    ]


admin.site.register(ProductCategory)
admin.site.register(ProductPriceChange)

admin.site.register(MultiProductCollectiveTracking)
