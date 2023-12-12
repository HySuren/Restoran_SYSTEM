from typing import List, Any, Dict
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Category, Goods, Order, Files


class DataBaseExemplar:
    def __init__(self):
        self.order = Order()
        self.goods = Goods()
        self.category = Category()


class WaiterChangeViews(DataBaseExemplar):
    def get_context(self) -> Dict[str, Any]:
        goods = Goods.objects.all()
        good_list = list(goods)

        categories = Category.objects.all()
        category_dict = {category.category_id: category.category_name for category in categories}

        categorized_goods = {category_id: [] for category_id in category_dict.keys()}

        for good in good_list:
            category_id = good.category_id
            categorized_goods[category_id].append({'title': good.title, 'price': good.price_rub})

        context = {
            'categories': category_dict,
            'categorized_goods': categorized_goods,
        }

        return context


class WaiterResponseView(WaiterChangeViews):
    @staticmethod
    def waiter_response(request) -> HttpResponse:
        waiter_change_view = WaiterChangeViews()
        context = waiter_change_view.get_context()
        return render(request, 'waiter.html', context)


class OrderCreateView(View):
    @csrf_exempt
    def create_order(request) -> JsonResponse:
        keys_list: List[str] = []
        values_list: List[Any] = []
        goods: str = ''
        sum_price: float = 0

        if request.method == 'POST':
            updated_data = json.loads(request.body.decode('UTF-8'))
            data = updated_data.get('values')
            for item in data:
                for key, value in item.items():
                    keys_list.append(key)
                    values_list.append(value)

            for value in values_list[0::2]:
                goods += f'{value}\n'

            for price in values_list[1::2]:
                sum_price += price

            order = Order(goods=goods, sum_price=sum_price, is_working=True)
            order.save()
            return JsonResponse({'status': 'success', 'redirect': 'waiter'})
        else:
            return JsonResponse({'status': 'error'})


class OrderChangeView(View):
    def get(self, request) -> JsonResponse:
        orders = Order.objects.all()
        data = list(orders.values())  # Convert QuerySet to list of dictionaries
        return JsonResponse({'data': data}, safe=False)


class OrderResponceViews(View):
    def get(self, request) -> HttpResponse:
        order_change_view = OrderChangeView()
        data = json.loads(order_change_view.get(request).content)
        context = {'data': data}
        return render(request, 'Orders.html', context)


class KitchenResponceViews(View):
    def get(self, request) -> HttpResponse:
        order_change_view = OrderChangeView()
        data = json.loads(order_change_view.get(request).content)
        context = {'data': data}
        return render(request, 'kitchen.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class OrderStateUpdate(View):
    def post(self, request) -> JsonResponse:
        data = json.loads(request.body.decode('utf-8'))
        order_id = data.get('OrderID')
        action_type = data.get('ActionType')

        order = Order.objects.get(pk=order_id)

        if action_type == 'ready':
            order.is_working = False
            order.is_ready = True
        elif action_type == 'delivered':
            order.is_working = False
            order.is_ready = False
            order.is_deleted = True

        order.save()
        return JsonResponse({'status': '200'})


class XlsxObjectCreator:
    def analitics_responce(self) -> HttpResponse:
        return render(self, 'analitics.html')


class XlsxObjectCreators(View):
    def get(self, request) -> JsonResponse:
        all_orders = Order.objects.all()
        file_obj = Files.create_excel_file(all_orders)
        return JsonResponse({'file_id': file_obj.id, 'file_path': file_obj.file.url})
