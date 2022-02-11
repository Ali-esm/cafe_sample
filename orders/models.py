from django.db import models

# Create your models here.
from model_utils import Choices

from core.models import BaseModel, BaseDiscount
from menu_items.models import MenuItem
from tables.models import Table

ORDER_STATUS = Choices(
    (0, 'CANCEL', 'Cancel'),
    (1, 'UNPAID', 'Unpaid'),
    (2, 'PAIN', 'Paid')
)


class Order(BaseModel):
    status = models.IntegerField(choices=ORDER_STATUS, default=ORDER_STATUS.UNPAID, verbose_name='Status')
    is_paid = models.BooleanField(default=False, verbose_name='Paid')
    table = models.ForeignKey(Table, on_delete=models.PROTECT, verbose_name='Table')
    off = models.ForeignKey('OffCode', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id} status :{self.status} '

    @property
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.order_items.all())

    @property
    def get_final_price(self):
        return self.get_total_cost - self.off.profit_value(self.get_total_cost)


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE, verbose_name='Order')
    item = models.ForeignKey(MenuItem, related_name='menu_items', on_delete=models.CASCADE,
                             verbose_name='Item')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Quantity')

    def __str__(self):
        return f"{self.quantity} * {self.item.name}"

    @property
    def get_cost(self):
        return (self.item.price - self.item.discount.profit_value(self.item.price)) * self.quantity


class OffCode(BaseModel, BaseDiscount):
    off_code = models.CharField(max_length=100, null=True, default='off')
    is_used = models.BooleanField(default=False)
