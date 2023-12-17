# Restoran_SYSTEM
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

#### GET-request to get all sent messages
    <host_ipv4>/api/v1/stat/sent

#### POST-request to send message to another copy of application
    <host_ipv4>/api/v1/send

### POST-request format
