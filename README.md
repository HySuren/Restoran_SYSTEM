# Restoran_SYSTEM
Приветсвую! Пару слов о самом проекте, проект представляет из себя внутренюю систему для для не большого кафе(реальный проект), поднят на https://api.dev.youthcafe.ru/waiter , можете перейти и посмотреть.\
Убедительная просьба не взаимодействовать там с системой так как она действительно используется и есть так же сбор статистики по заказам за смену, да бы мне не приходилось после отчитыватся ;)\
Продолжим...\
Все мы бываем в KFC,Burger King и.т.д, и у них есть табло где отображается состояние заказа, и свое внутренее приложение для сотрудников, моя система можно сказать аналог этих систем.
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
#### Send request
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
#### Processing on the server

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

#### POST-request to send message to another copy of application
    <host_ipv4>/api/v1/send

### POST-request format
