from django.contrib import admin
from products.models import Product, ProductCategory, ProductPriceChange


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'price', 'target_price', 'availability', 'user')
    ordering = ('site', 'name')
    list_filter = ('availability_message',)
    search_fields = ('url', 'name')


admin.site.register(ProductCategory)
admin.site.register(ProductPriceChange)
