# Generated by Django 4.2.8 on 2023-12-10 12:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClientAPI', '0010_alter_order_datetimes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='datetimes',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 10, 15, 59, 17, 287950), verbose_name='datetimes'),
        ),
        migrations.RemoveField(
            model_name='order',
            name='goods',
        ),
        migrations.AddField(
            model_name='order',
            name='goods',
            field=models.TextField(default=2, verbose_name='goods'),
            preserve_default=False,
        ),
    ]
