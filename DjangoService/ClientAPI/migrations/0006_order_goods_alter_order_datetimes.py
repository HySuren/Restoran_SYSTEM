# Generated by Django 4.2.8 on 2023-12-07 20:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClientAPI', '0005_alter_order_datetimes'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='goods',
            field=models.JSONField(default=2, verbose_name='goods'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='datetimes',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 7, 20, 17, 44, 381158, tzinfo=datetime.timezone.utc), verbose_name='datetimes'),
        ),
    ]
