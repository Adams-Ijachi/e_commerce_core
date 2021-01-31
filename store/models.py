from django.db import models
from django.shortcuts import reverse
from accounts.models import Agent , Customer 
from .utils import unique_transaction_id_generator
from django.db.models.signals import pre_save
from django.conf import settings
# Create your models here.

order_status = (
    ('P','Pending'),
    ('C','created'),
    ('R','reviwed')

)

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name



class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(verbose_name='Product_Image',upload_to='img/products', null=True, blank=True)
    price = models.FloatField()
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True,)
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:product_detail', kwargs={'pk':self.id})
   
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    

class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True,blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    billing_address = models.ForeignKey('ShippingAddress',on_delete=models.SET_NULL, blank=True, null=True)
    completed = models.BooleanField(default=False, null=True, blank=False)
    order_reviewed = models.BooleanField(default=False, null=True, blank=False)
    order_status = models.CharField(max_length=10, default='C', choices=order_status)



    def __str__(self):
        return self.customer.email

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_count_total(self):
        orderitems = self.orderitem_set.all()
        total = len(orderitems)
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


    @classmethod
    def pre_save_create_order_id(self,sender, instance, *args, **kwargs):
        if not instance.transaction_id:
            instance.transaction_id= unique_transaction_id_generator(instance)


pre_save.connect(Order.pre_save_create_order_id, sender=Order)

class OrderItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total 

class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200,verbose_name="Address")
    apartment_address = models.CharField(max_length=200, verbose_name="Address 2", blank=True)

    def __str__(self):
        return self.user.email







         


    
    