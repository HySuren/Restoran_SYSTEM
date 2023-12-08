from django.shortcuts import render
from .models import Category, Goods, Order
from typing import List, Any


class DataBaseExemplar:
    def __init__(self):
        self.order = Order()
        self.goods = Goods()
        self.category = Category()


class MainRenderViews:
    @staticmethod
    def main_documents(request):
        return render(request, 'main.html')


class WaiterChangeViews(DataBaseExemplar):
    def get_context(self):
        goods = Goods.objects.all()
        categories = Category.objects.all()

        good_list: List[Any] = list(goods)
        category_list: List[Any] = list(categories)

        context = {
            'goods': good_list,
            'category': category_list
        }

        return context


class WaiterResponseView(WaiterChangeViews):
    @staticmethod
    def waiter_response(request):
        waiter_change_view = WaiterChangeViews()
        context = waiter_change_view.get_context()
        return render(request, 'waiter.html', context)