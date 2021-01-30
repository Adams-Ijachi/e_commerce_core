from django.shortcuts import render , get_object_or_404 
from .models import *
from django.http import JsonResponse
import json


# Create your views here.
def home_view(request):
    products = Products.objects.all()
    categories = Category.objects.all()
    context = {'products':products,'categories':categories}
    return render(request, 'store/index.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Products, pk=pk)
    context = {'product':product}
    return render(request, 'store/product-page.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
    else:
        items =[]
        order =  {'get_cart_total':0, 'get_cart_items':0}
    context = {'items':items, 'order':order}
    return render(request, 'store/cart.html', context)



def checkout_summary(request):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
    else:
        items =[]
        order =  {'get_cart_total':0, 'get_cart_items':0}
    context = {'items':items, 'order':order}
    return render(request, 'store/checkout-page.html', context)


def updateitem(request):
    if request.user.is_authenticated:

        productId = request.POST['productId']
        action = request.POST['action']
        customer = request.user
        product = Products.objects.get(id=productId)
        order, create = Order.objects.get_or_create(customer=customer, completed=False, order_reviewed=False)
        orderitem , created = OrderItem.objects.get_or_create(product=product, order=order)

        if action == 'add':
            orderitem.quantity += 1
            orderitem.save()
            data = {'action':'cart-update','orderitem_count':order.get_cart_count_total,'order_total':order.get_cart_total,'orderitem_price':orderitem.get_total}
            return JsonResponse(data, safe=False)
      
        elif action == 'remove':
            orderitem.delete()
            data = {'action':'cart-update','orderitem_count':order.get_cart_count_total}
            return JsonResponse(data,safe=False )
        elif action=='remove-product':
            orderitem.delete()
            data = {'action':'cart-product-update','orderitem_count':order.get_cart_count_total,'order_total':order.get_cart_total}
            return JsonResponse(data, safe=False)
        elif action == 'quantity-add':
            orderitem.quantity += 1
            orderitem.save()
            data = {'action':'quantity-upadate','order_total':order.get_cart_total,'orderitem_price':orderitem.get_total,'orderitem_quantity':orderitem.quantity}
            return JsonResponse(data, safe=False)
        elif action == 'quantity-remove':
            orderitem.quantity -= 1
            orderitem.save()
            data = {'action':'quantity-upadate','order_total':order.get_cart_total,'orderitem_price':orderitem.get_total,'orderitem_quantity':orderitem.quantity}
            return JsonResponse(data, safe=False)



        
    else:
        return JsonResponse("Login needed", safe=False,status=401)

# def itemQuantity(request):
#     if request.user.is_authenticated:

