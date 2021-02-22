from django.shortcuts import render , get_object_or_404  , redirect
from django.core.paginator import Paginator,  EmptyPage,PageNotAnInteger
from .form import Shipping_address
from django.http import JsonResponse , HttpResponse
from .models import *
import json


# Create your views here.
def home_view(request):
    products = Products.objects.all().order_by('-id')
    categories = Category.objects.all()
    page = request.GET.get('page',1)
    paginator = Paginator(products,1)
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page()
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    context = {'products':products_page,'categories':categories}
   
    return render(request, 'store/index.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Products, pk=pk)
    context = {'product':product}
    return render(request, 'store/product-page.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer=customer, completed=False,order_status='C')
        items = order.orderitem_set.all()
    else:
        items =[]
        order =  {'get_cart_total':0, 'get_cart_items':0}
    context = {'items':items, 'order':order}
    return render(request, 'store/cart.html', context)



def checkout_summary(request):
    form = Shipping_address(request.POST or None)
    if request.method == 'POST' and request.user.is_authenticated:
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save() 
            order = get_object_or_404(Order,  customer=request.user, completed=False, order_reviewed=False, order_status='C')
            order.billing_address = obj
            order.order_status = 'P'
            order.save()
            return HttpResponse('order process view in dashboard')

    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer=customer, completed=False, order_reviewed=False ,order_status='C')
        items = order.orderitem_set.all()
    else:
        items =[]
        order =  {'get_cart_total':0, 'get_cart_items':0}
    context = {'items':items, 'order':order, 'form':form}

    return render(request, 'store/checkout-page.html', context)


def updateitem(request):
    if request.user.is_authenticated:

        productId = request.POST['productId']
        action = request.POST['action']
        customer = request.user
        product = Products.objects.get(id=productId)
        order, create = Order.objects.get_or_create(customer=customer, completed=False, order_reviewed=False, order_status='C')
        orderitem , created = OrderItem.objects.get_or_create(product=product, order=order)

        if action == 'add':
            orderitem.quantity += 1
            orderitem.save()
            data = {'action':'cart-update','orderitem_count':order.get_cart_count_total,'order_total':order.get_cart_total,'orderitem_price':orderitem.get_total}
            
      
        elif action == 'remove':
            orderitem.delete()
            data = {'action':'cart-update','orderitem_count':order.get_cart_count_total}
            
        elif action=='remove-product':
            orderitem.delete()
            data = {'action':'cart-product-update','orderitem_count':order.get_cart_count_total,'order_total':order.get_cart_total}
            
        elif action == 'quantity-add':
            orderitem.quantity += 1
            orderitem.save()
            data = {'action':'quantity-upadate','order_total':order.get_cart_total,'orderitem_price':orderitem.get_total,'orderitem_quantity':orderitem.quantity,'orderitem_count':order.get_cart_count_total}
            
        elif action == 'quantity-remove':
            orderitem.quantity -= 1
            orderitem.save()
            data = {'action':'quantity-upadate','order_total':order.get_cart_total,'orderitem_price':orderitem.get_total,'orderitem_quantity':orderitem.quantity,'orderitem_count':order.get_cart_count_total}
        if orderitem.quantity <=0:
            orderitem.delete()
            data = {'action':'quantity-upadate','order_total':order.get_cart_total,'orderitem_price':orderitem.get_total,'orderitem_quantity':0,'orderitem_count':order.get_cart_count_total,'orderitem_count':order.get_cart_count_total}
        return JsonResponse(data, safe=False)        
    else:
        return JsonResponse("Login needed", safe=False,status=401)


def search(request):
    try:
       q  = request.GET['q']
    except:
        q = None
    if q:  
       product = Products.objects.filter(name__icontains=q)
       context = {'products':product,'product_name':q}
       return render(request, 'store/search-product.html', context)
    return redirect(reverse('core:home'))
    
  


def products_page(request):
    name  = request.GET['name']
    return HttpResponse(f'the name is {name}')
        


