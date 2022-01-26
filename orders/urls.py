from django.urls import path
from .views import OrderItemCreateView


urlpatterns = [
    path('create-order/', OrderItemCreateView.as_view(), name='create_order'),
]