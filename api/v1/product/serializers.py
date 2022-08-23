from rest_framework import serializers
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):

    # def update_or_create(self, validated_data):
    #     if Product.objects.filter(name=validated_data.get('name'), url=validated_data.get('url')):
    #         Product.objects.filter(name=validated_data.get('name'), url=validated_data.get('url'))[0].update(data=validated_data)
    #     else:
    #         Product.objects.create(data=validated_data)

    class Meta:
        model = Product
        fields = "__all__"
        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset=Product.objects.all(),
        #         fields=['name', 'url', 'user']
        # )]
