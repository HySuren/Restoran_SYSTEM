from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path,re_path
from ClientAPI.views import WaiterResponseView,OrderCreateView\
    ,OrderResponceViews,OrderChangeView,KitchenResponceViews,\
    OrderStateUpdate,XlsxObjectCreator,XlsxObjectCreators
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('waiter', WaiterResponseView.waiter_response),
    path('create_order', OrderCreateView.create_order,name='new_order'),
    path('order', OrderResponceViews.as_view(), name='order_response'),
    path('data_order/', OrderChangeView.as_view(), name='data_order'),
    path('kitchen', KitchenResponceViews.as_view(), name='kitchen'),
    path('order_update', OrderStateUpdate.as_view(), name='order_update'),
    path('download_excel/',XlsxObjectCreators.as_view(), name='download_excel'),
    path('analitic', XlsxObjectCreator.analitics_responce, name='download_excel'),
    re_path(r'^(?P<path>.*)/$', lambda request, path: HttpResponseRedirect("/%s" % path)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)