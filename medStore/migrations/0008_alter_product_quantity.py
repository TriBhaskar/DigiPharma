# Generated by Django 4.0.6 on 2022-09-15 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medStore', '0007_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=1, null=True),
        ),
    ]