from django.db import models
from django.shortcuts import reverse
# from accounts

# Create your models here.

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
    

# class OrderItem(models.Model):

    
    