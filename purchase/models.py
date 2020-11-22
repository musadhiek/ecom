from django.db import models
from .models import *
from django.contrib.auth.models import User
from product.models import Product


class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    phone = models.CharField(max_length=15 ,null=True,blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200,null=True)
    pincode = models.CharField(max_length=10,null=True)
    default_address = models.BooleanField(default=False)

class OrderItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    quantity =models.IntegerField(default=1,null=True,blank=True)
    price = models.DecimalField(decimal_places=2,max_digits=20,null=True,blank=True)
# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user',null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    # vendor = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='vendor',blank=True)
    orderitem = models.ForeignKey(OrderItem,on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.IntegerField(default=1,null=True,blank=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200,null=True)
    delivered = models.BooleanField(default=False)
    delivery_address = models.ForeignKey(ShippingAddress,on_delete=models.SET_NULL,blank=True,null=True)




    # @property
    # def get_total (self):
    #     total = self.product.price * quantity
    #     return total



