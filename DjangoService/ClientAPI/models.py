from django.db import models
from typing import Text
import datetime



class Category(models.Model):
    category_id: int = models.AutoField(primary_key=True)
    category_name: Text = models.TextField('category_name', max_length=255, unique=True, null=False,
                                           default='Новая категория')

    class Meta:
        db_table = 'Category'

    def __str__(self):
        return self.category_name


class Goods(models.Model):
    goods_id: int = models.AutoField(primary_key=True)
    title: Text = models.CharField('title', max_length=255, null=False, default='Без названия')
    description: Text = models.TextField('description', max_length=255,default='.')
    price_rub: int = models.FloatField('price_rub', null=False, default=0.00)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

    class Meta:
        db_table = 'Goods'

    def __str__(self):
        return f'{self.title}\n{self.description}'


class Order(models.Model):
    order_id: int = models.AutoField(primary_key=True)
    goods = models.ManyToManyField('Goods')
    datetimes: datetime = models.DateTimeField('datetimes', default=datetime.datetime.now())
    sum_price: int = models.FloatField('sum_price', null=False, default=0.00)
    is_working: bool = models.BooleanField('is_working', default=False)  # This trigger if the value of the object -
    # is true,then the order will be displayed in the state 'At work'
    is_ready: bool = models.BooleanField('is_ready', default=False)  # This trigger if the value of the object -
    # is true, the order will be displayed in the 'Ready' state
    is_deleted: bool = models.BooleanField('is_deleted', default=False)  # This trigger if the value of the object -

    # is true, the order will not be displayed, and will be transferred to the archive
    class Meta:
        db_table = 'Order'
