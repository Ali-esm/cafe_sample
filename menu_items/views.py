from django.shortcuts import render
from django.views import generic
from .models import MenuItem


# Create your views here.
class MenuItemListView(generic.ListView):
    model = MenuItem
    template_name = 'menu_items/menu_item/sample.html'
