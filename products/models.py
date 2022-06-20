from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse, reverse_lazy
from django.conf import settings
from products.constants import WEBSITE_CHOICES


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
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, blank=True, null=True)
    price = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    max_price = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    min_price = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    target_price = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    rating = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True)
    ratings_count = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    reviews_count = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    availability_message = models.CharField(max_length=100, null=True, blank=True)
    availability = models.BooleanField(default=True, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

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

    def save(self, *args, **kwargs):
        if self.price is not None:
            if self.max_price is None:
                self.max_price = self.price
            if self.min_price is None:
                self.min_price = self.price
        super().save(*args, **kwargs)


class ProductPriceChange(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, editable=True)
    price = models.IntegerField()

    class Meta:
        unique_together = ['product', 'date']

    def __str__(self) -> str:
        return f'{self.date} > {self.product.name}'
