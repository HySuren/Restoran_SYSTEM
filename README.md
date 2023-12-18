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
    127.0.0.1:8000/data_order
