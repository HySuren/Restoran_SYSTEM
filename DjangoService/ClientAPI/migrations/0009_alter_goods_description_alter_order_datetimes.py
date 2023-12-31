# Generated by Django 4.2.8 on 2023-12-07 20:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClientAPI', '0008_alter_goods_description_alter_order_datetimes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='description',
            field=models.TextField(default='.', max_length=255, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='order',
            name='datetimes',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 7, 20, 42, 39, 566341, tzinfo=datetime.timezone.utc), verbose_name='datetimes'),
        ),
    ]
