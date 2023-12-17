# Generated by Django 4.2.8 on 2023-12-07 20:12

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ClientAPI', '0002_remove_order_goods_alter_order_datetimes'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='goods',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='ClientAPI.goods'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='datetimes',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 7, 20, 12, 1, 9313, tzinfo=datetime.timezone.utc), verbose_name='datetimes'),
        ),
    ]