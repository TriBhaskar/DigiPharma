# Generated by Django 4.0.6 on 2022-08-21 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medStore', '0005_alter_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]