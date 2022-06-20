from django.db.models.signals import post_save
from django.dispatch import receiver
from scripts.update_product import update_product_data
from products.models import Product


# @receiver(post_save, sender=Product)
# def update_product(sender, instance, **kwargs):
#     instance.availability_message = 'killer app'
#     instance.save()
#
# def say_hello(sender, instance, **kwargs):
#     response = update_product_data(instance.id, data={'availability_message': 'another killer feature'})
#     print(response)