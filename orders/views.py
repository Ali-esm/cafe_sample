from django.views import generic
from .models import OrderItem, Order


# Create your views here.
class OrderItemCreateView(generic.CreateView):
    model = OrderItem
    fields = ['item', 'quantity', 'order']
    template_name = 'orders/create_order_item.html'

    success_url = '/create-order/'

