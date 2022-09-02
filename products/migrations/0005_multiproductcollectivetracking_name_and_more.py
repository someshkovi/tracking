# Generated by Django 4.0.5 on 2022-09-01 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_multisitetracking'),
    ]

    operations = [
        migrations.AddField(
            model_name='multiproductcollectivetracking',
            name='name',
            field=models.CharField(default='p1', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='only_for_search',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='site',
            field=models.CharField(blank=True, choices=[('amazon.in', 'amazon'), ('flipkart.com', 'flipkart'), ('amazon.com', 'amazon us')], max_length=20, null=True),
        ),
    ]
