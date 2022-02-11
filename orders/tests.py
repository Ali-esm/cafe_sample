from django.test import TestCase


# Create your tests here.
from menu_items.models import Category, Discount
from orders.models import Order, OrderItem, OffCode, MenuItem
from tables.models import Table


class OrderTest(TestCase):

    def setUp(self):
        # SetUp Table
        self.tbl = Table.objects.create(capacity=1)

        # SetUp Discount
        self.discount1 = Discount.objects.create(amount=0, type='price')
        self.discount2 = Discount.objects.create(amount=0, type='percent')
        self.discount3 = Discount.objects.create(amount=10, type='percent', max_price=20000)
        self.discount4 = Discount.objects.create(amount=10000, type='price')
        self.discount5 = Discount.objects.create(amount=40, type='percent', max_price=100000)

        # SetUp OffCode
        self.off1 = OffCode.objects.create(amount=20000, type='price')
        self.off2 = OffCode.objects.create(amount=20, type='percent', max_price=40000)

        # SetUp Category
        self.cat1 = Category.objects.create(name='cat1')

        # SetUp MenuItem
        self.item1 = MenuItem.objects.create(name='item1', category=self.cat1, price=10000, discount=self.discount1)
        self.item2 = MenuItem.objects.create(name='item2', category=self.cat1, price=300000)
        self.item3 = MenuItem.objects.create(name='item3', category=self.cat1, price=40000, discount=self.discount3)

        # SetUp Order
        self.order1 = Order.objects.create(table=self.tbl)
        self.order2 = Order.objects.create(table=self.tbl, off=self.off2)

        # setUp OrderItem
        self.orderitems1 = OrderItem(order=self.order1, item=self.item1)
        self.orderitems2 = OrderItem(order=self.order2, item=self.item3)

    def test_discount_amount_0(self):
        self.assertEqual(self.discount1.profit_value(100000), 0)
        self.assertEqual(self.discount2.profit_value(150000), 0)

    def test_profit_value_15000(self):
        self.assertEqual(self.discount3.profit_value(15000), 1500)
        self.assertEqual(self.discount4.profit_value(15000), 10000)
        self.assertEqual(self.discount5.profit_value(15000), 6000)

    def test_order_items_get_cost(self):
        self.assertEqual(self.orderitems1.get_cost, 10000)
        self.assertEqual(self.orderitems2.get_cost, 36000)

