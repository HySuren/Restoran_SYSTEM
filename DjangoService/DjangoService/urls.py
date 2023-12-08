from django.contrib import admin
from django.urls import path
from ClientAPI.views import MainRenderViews, WaiterResponseView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainRenderViews.main_documents),
    path('waiter', WaiterResponseView.waiter_response),
]
