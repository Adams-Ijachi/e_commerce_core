from django import template 
from django.shortcuts import render , get_object_or_404 
from store.models import Order
register = template.Library()

@register.filter
def cart_counter(user):
    if user.is_authenticated:
    
        order_qs = Order.objects.filter(customer=user, completed=False, order_status='C')
    
        if order_qs.exists():
            order = get_object_or_404(Order, customer=user, completed=False, order_status='C')
         
            return order.get_cart_count_total
        return 0
    return 0