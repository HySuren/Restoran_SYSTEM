# Restoran_SYSTEM
Приветсвую! Пару слов о самом проекте, проект представляет из себя внутренюю систему для для не большого кафе
Все мы бываем в KFC,Burger King и.т.д, и у них есть табло где отображается состояние заказа, и свое внутренее приложение для сотрудников, мой сервис можно сказать является их копиями созданной для этого кафе.
***
api.dev.youthcafe.ru Убедительная просьба не взаимодействовать на сайте,так как он используется для работы, и есть функция скачивания .xlsx файлов со статистикой.\
Для тестов просьба клонировать репозиторий запустить и тестировать.
***
Заказчикам был нужен сервис максимально похожий, и я предложил им свое решение(возможно далеко не идеальное) так как я планирую обновлять этот сервис, но его приняли и сейчас используют для работы\
Главной сутью было создать тот самый эффект динамического обновления данных на всех 3 интерфейсах(приемка,табло состояния заказов,кухня/выдача).
Тут думаю ясно, если приемка создает заказ то тут же данные отображаются в общем табло(состояние: В работе), и в 'Кухне', и соответсвенно при всех прочих взаимодейстиях та же логика.\
Для получения обновленных данных я использовал Ajax-запросы чтобы раз в 1сек,отправлять запрос на условно https:\\api.dev.youthcafe.ru\data_order , и получать от сервера информацию о всех заказах.\
То же самое если нужно не получить а создать или изменить(состояние) заказ/а.
***
'Ниже есть API endpoint где можно увидеть что происходит при отправке запроса на тот или иной url'
***
## Stack
### Backend
    Python
    Django
    openpyxl
    psycopg2
### Frontend
    HTML
    CSS
    SCSS
    JS
    Ajax
    JQuery
### Web-server
    Nginx
### WSGI-server
    Gunicorn
### Data Base
    PostgreSQL
***
## Repository content
    
- ./requirements.txt - a set of modules required for the application
- ./ClientAPI/ - Django app 
- ./DjangoService/ - source directory
- ./manage.py - application startup script

***
## Startup Examples
### Windows
#### Step 1
    pip install -r requirements.txt
#### Step 2
    python manage.py makemigrations
#### Step 3
    python manage.py migrate
#### To run 
    python manage.py runserver 

### Linux
#### Step 1
    pip3 install -r requirements.txt
#### Step 2
    python3 manage.py makemigrations
#### Step 3
    python3 manage.py migrate
#### To run 
    python3 manage.py runserver 
***
### API endpoints
#### GET-request to get waiter.html and waiter.css
    127.0.0.1:8000/waiter

```python
class WaiterChangeViews(DataBaseExemplar):
    """Handles logic related to data needed for the waiter interface."""
    def get_context(self) -> Dict[str, Any]:
        """Get context data for rendering the waiter interface."""
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
    """Handles HTTP requests for the waiter interface."""
    @staticmethod
    def waiter_response(request) -> HttpResponse:
        """Handles the HTTP GET request and renders the waiter interface."""
        waiter_change_view = WaiterChangeViews()
        context = waiter_change_view.get_context()
        return render(request, 'waiter.html', context)
```

#### POST-request to create new order
    127.0.0.1:8000/create_order
```
{
            values: previousValues < str >,
            totalAmount: totalAmount < float >
        }
```
##### Send request
```
        $('#submitValues').click(function(){
        var dataToSend = {
            values: previousValues,
            totalAmount: totalAmount
        };

        $.ajax({
            type: "POST",
            url: "create_order",
            data: JSON.stringify(dataToSend), // отправляем данные в формате JSON
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data){
                if (data.status === 'success') {
                    console.log("Данные успешно отправлены:", data);
```
##### Processing on the server

```python
class OrderCreateView(View):
    """Handles creating new orders."""
    @csrf_exempt
    def create_order(request) -> JsonResponse:
        """Handles the HTTP POST request to create a new order."""
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
```

#### GET-request to all orders
    127.0.0.1:8000/data_order
##### Send request
```
    $(document).ready(function () {
    function fetchData() {
        $.ajax({
            url: '/data_order',
            type: 'GET',
            success: function (data) {
                updateOrders(data);
            },
            error: function (error) {
                console.error('Error fetching data:', error);
            }
        });
    }
    ...
```
##### Processing on the server
```python
    class OrderChangeView(View):
    def get(self, request) -> JsonResponse:
        orders = Order.objects.all()
        data = list(orders.values())  # Convert QuerySet to list of dictionaries
        return JsonResponse({'data': data}, safe=False)
```
### GET-request to get kithen.html and kithen.css
    127.0.0.1:8000/kitchen
##### Processing on the server
```python
class KitchenResponceViews(View):
    def get(self, request) -> HttpResponse:
        order_change_view = OrderChangeView()
        data = json.loads(order_change_view.get(request).content)
        context = {'data': data}
        return render(request, 'kitchen.html', context)
```
### UPDATE-request to state Order
    127.0.0.1:8000/order_update
##### Send request
```
 // Обработчик кнопок "Готово" и "Выдано"
            $(document).on('click', '.btnReady, .btnDelivered', function () {
                var orderId = $(this).data('orderid');
                var actionType = $(this).hasClass('btnReady') ? 'ready' : 'delivered';

                // Вызов функции обработки на сервере с orderId и actionType в теле запроса
                $.ajax({
                    url: 'order_update',
                    type: 'POST',
                    contentType: 'application/json', // Set content type to JSON
                    data: JSON.stringify({ OrderID: orderId, ActionType: actionType }), // Convert data to JSON string
                    success: function (response) {
                        // Обновление данных после успешного обновления на сервере
                        fetchData();
                    },
                    error: function (error) {
                        console.error('Error marking order as ready or delivered:', error);
                    }
                });
            });

            setInterval(function () {
                $.ajax({
                    url: '/data_order',
                    type: 'GET',
                    success: function (data) {
                        updateOrders(data);
                        checkOverflow();
                    },
                    error: function (error) {
                        console.error('Error fetching data:', error);
                    }
                });
            }, 1000);
```
##### Processing on the server
```python
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
```
### GET-request to get .xlsx file statistic all order
##### Send request
```
function isDownload() {
    $.ajax({
        url: 'download_excel/',  
        type: 'GET',
        success: function(response) {
            if ('error' in response) {
                console.error('Ошибка при загрузке файла:', response.error);
            } else {
                // Создаем ссылку для скачивания
                var downloadLink = document.createElement('a');
                downloadLink.href = response.file_path;
                downloadLink.download = 'orders_report.xlsx';

                // Добавляем ссылку в DOM и автоматически щелкаем по ней
                document.body.appendChild(downloadLink);
                downloadLink.click();
                document.body.removeChild(downloadLink);
            }
        },
        error: function(error) {
            console.error('Ошибка при загрузке файла:', error);
        }
    });
}
```
##### Processing on the server
```python
class XlsxObjectCreators(View):
    def get(self, request) -> JsonResponse:
        all_orders = Order.objects.all()
        file_obj = Files.create_excel_file(all_orders)
        return JsonResponse({'file_id': file_obj.id, 'file_path': file_obj.file.url})
```
##### models.py Files
```python
class Files(models.Model):
    file = models.FileField(upload_to='orders_files/', null=True, blank=True)

    class Meta:
        db_table = 'Files'

    def __str__(self):
        return f'File {self.id}'

    @staticmethod
    def create_excel_file(orders: List[Order]) -> 'Files':
        # Create an Excel file and save it in a BytesIO object
        content_file = BytesIO()
        wb = Workbook()
        ws = wb.active

        # Increase the column sizes
        ws.column_dimensions['A'].width = 15
        ws.column_dimensions['B'].width = 25
        ws.column_dimensions['C'].width = 50
        ws.column_dimensions['D'].width = 15

        # Column headers
        ws.append(['Номер заказа', 'Дата создания и время', 'Перечень', 'Итоговая сумма'])

        for order in orders:
            # Create a new row in each iteration of the loop
            row = [
                order.order_id,
                localtime(order.datetimes).replace(tzinfo=None),
                '\n'.join(order.goods.split('\n')),
                order.sum_price
            ]
            ws.append(row)

        # Add a formula to sum the "Итоговая сумма" column
        last_row = len(orders) + 2
        ws.cell(row=last_row, column=3, value=f'Итог:')
        ws.cell(row=last_row, column=4, value=f'=SUM(D2:D{last_row - 1})')

        # Highlight only the last cell "Итоговая сумма" in yellow
        last_cell = ws.cell(row=last_row, column=4)
        last_cell.fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

        last_cell_two = ws.cell(row=last_row, column=3)
        last_cell_two.fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

        # Output the contents of orders and content_file for debugging
        #print("Orders:", orders)
        #print("Content File:", content_file.getvalue())

        # Save the file in the BytesIO object
        wb.save(content_file)

        # Save the file in the Files model
        obj = Files.objects.create()
        obj.file.save('orders_report.xlsx', ContentFile(content_file.getvalue()), save=True)

        return obj
```
***
### Models
```python
from typing import Text, List
import datetime
from django.db import models
from django.core.files.base import ContentFile
from openpyxl import Workbook
from django.utils.timezone import localtime
from openpyxl.styles import PatternFill
from io import BytesIO

offset = datetime.timezone(datetime.timedelta(hours=6))


class Category(models.Model):
    category_id: int = models.AutoField(primary_key=True)
    category_name: Text = models.TextField('category_name', max_length=255, unique=True, null=False, default='Новая категория')

    class Meta:
        db_table = 'Category'

    def __str__(self):
        return self.category_name


class Goods(models.Model):
    goods_id: int = models.AutoField(primary_key=True)
    title: Text = models.CharField('title', max_length=255, null=False, default='Без названия')
    description: Text = models.TextField('description', max_length=255, default='.')
    price_rub: int = models.FloatField('price_rub', null=False, default=0.00)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

    class Meta:
        db_table = 'Goods'

    def __str__(self):
        return f'{self.title}............. {self.price_rub}руб'


class Order(models.Model):
    order_id: int = models.AutoField(primary_key=True)
    goods: Text = models.TextField('goods')
    datetimes: datetime = models.DateTimeField('datetimes', default=datetime.datetime.now(offset))
    sum_price: int = models.FloatField('sum_price', null=False, default=0.00)
    is_working: bool = models.BooleanField('is_working', default=False)
    is_ready: bool = models.BooleanField('is_ready', default=False)
    is_deleted: bool = models.BooleanField('is_deleted', default=False)

    class Meta:
        db_table = 'Order'


class Files(models.Model):
    file = models.FileField(upload_to='orders_files/', null=True, blank=True)

    class Meta:
        db_table = 'Files'

    def __str__(self):
        return f'File {self.id}'

    @staticmethod
    def create_excel_file(orders: List[Order]) -> 'Files':
        # Create an Excel file and save it in a BytesIO object
        content_file = BytesIO()
        wb = Workbook()
        ws = wb.active

        # Increase the column sizes
        ws.column_dimensions['A'].width = 15
        ws.column_dimensions['B'].width = 25
        ws.column_dimensions['C'].width = 50
        ws.column_dimensions['D'].width = 15

        # Column headers
        ws.append(['Номер заказа', 'Дата создания и время', 'Перечень', 'Итоговая сумма'])

        for order in orders:
            # Create a new row in each iteration of the loop
            row = [
                order.order_id,
                localtime(order.datetimes).replace(tzinfo=None),
                '\n'.join(order.goods.split('\n')),
                order.sum_price
            ]
            ws.append(row)

        # Add a formula to sum the "Итоговая сумма" column
        last_row = len(orders) + 2
        ws.cell(row=last_row, column=3, value=f'Итог:')
        ws.cell(row=last_row, column=4, value=f'=SUM(D2:D{last_row - 1})')

        # Highlight only the last cell "Итоговая сумма" in yellow
        last_cell = ws.cell(row=last_row, column=4)
        last_cell.fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

        last_cell_two = ws.cell(row=last_row, column=3)
        last_cell_two.fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

        # Output the contents of orders and content_file for debugging
        #print("Orders:", orders)
        #print("Content File:", content_file.getvalue())

        # Save the file in the BytesIO object
        wb.save(content_file)

        # Save the file in the Files model
        obj = Files.objects.create()
        obj.file.save('orders_report.xlsx', ContentFile(content_file.getvalue()), save=True)

        return obj

```
