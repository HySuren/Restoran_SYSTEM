# Generated by Django 4.2.8 on 2023-12-12 16:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClientAPI', '0016_alter_order_datetimes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='datetimes',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 12, 16, 49, 31, 180613, tzinfo=datetime.timezone.utc), verbose_name='datetimes'),
        ),
    ]