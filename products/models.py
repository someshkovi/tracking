import datetime
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse, reverse_lazy
from django.conf import settings
from products.constants import WEBSITE_CHOICES
from django.contrib import admin


class TimestampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProductCategory(models.Model):
    category = models.CharField(max_length=50, unique=True)
    sub_category = models.CharField(max_length=50)

    class Meta:
        unique_together = ('category', 'sub_category',)
        ordering = ('category', 'sub_category')

    def __str__(self) -> str:
        return f'{self.category} > {self.sub_category}'


class Product(TimestampModel):
    url = models.URLField(max_length=1000, blank=True, null=True)
    site = models.CharField(max_length=20, choices=WEBSITE_CHOICES, blank=True, null=True)
    is_url_valid = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    name_in_site = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, blank=True, null=True)
    price = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    max_price = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    min_price = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    target_price = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    rating = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True)
    ratings_count = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    reviews_count = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    availability_message = models.CharField(max_length=100, null=True, blank=True)
    availability = models.BooleanField(default=False)
    only_for_search = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.price is not None:
            if self.max_price is None:
                self.max_price = self.price
            else:
                self.max_price = max(self.max_price, self.price)
            if self.min_price is None:
                self.min_price = self.price
            else:
                self.min_price = min(self.min_price, self.price)

            # # add historic data to ProductPriceChange model
            # # new_obj, created = statement can be used to check if its created
            # # ProductPriceChange.objects.get_or_create(product=self, price=self.price, date=datetime.date.today())
            # if not len(ProductPriceChange.objects.filter(product=self, date=datetime.date.today())):
            #     ProductPriceChange.objects.create(product=self, price=self.price, date=datetime.date.today())

        if self.name_in_site is None and self.name is not None:
            self.name_in_site = self.name
        if self.name is None and self.name_in_site is not None:
            self.name = self.site_name

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.name}'

    def get_absolute_url(self):
        if self.pk:
            return reverse("products:product-detail", kwargs={"pk": self.pk})
        return reverse_lazy('products:products-list')

    def get_edit_url(self):
        if self.pk:
            return reverse('products:product-update', kwargs={'pk': self.pk})
        return reverse_lazy('products:products-list')

    @admin.display(
        boolean=True,
    )
    def is_price_below_target_price(self):
        if None not in (self.target_price, self.price):
            return self.target_price <= self.price
        return False

    @admin.display(
        boolean=True,
    )
    def is_at_lowest_price(self):
        if None not in (self.price, self.max_price, self.min_price):
            return self.min_price < self.max_price and self.min_price <= self.price
        return False


class ProductPriceChange(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, editable=True)
    price = models.IntegerField()

    class Meta:
        unique_together = ['product', 'date']

    def __str__(self) -> str:
        return f'{self.date} > {self.product.name}'


@receiver(post_save, sender=Product)
def save_profile(sender, instance, **kwargs):
    if instance.price is not None:
        if not len(ProductPriceChange.objects.filter(product=instance, date=datetime.date.today())):
            ProductPriceChange.objects.create(product=instance, price=instance.price, date=datetime.date.today())


class MultiProductCollectiveTracking(models.Model):
    products = models.ManyToManyField(Product)
    total_price = models.IntegerField(blank=True, null=True)
    total_target_price = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class MultiSiteTracking(models.Model):
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
