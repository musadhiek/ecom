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

    def __str__(self):
        return self.address



class Order(models.Model):
    ORDER_NOT_PLACED= 1
    ORDER_PLACED = 2
    ORDER_CANCELLED = 3

    NOT_PAID = 1 
    PAYMENT_PENDING= 2
    PAID = 3

    
    ORDER_ACCEPTED = 1
    ORDER_DISPATCHED = 2
    ORDER_DELIVERED = 3
    ORDER_CANCELLED = 4

    ORDER_CHOICES =((ORDER_NOT_PLACED,'Order Not Placed'),(ORDER_PLACED,'Order Placed' ),(ORDER_CANCELLED,'Order Cancelled'))
    PAYMENT_CHOICES =((NOT_PAID,'Not Paid' ),(PAYMENT_PENDING,'Payment Pending'),(PAID,'Paid'))
    DELIVERY_CHOICES =((ORDER_ACCEPTED,'Order Accepted' ),(ORDER_DISPATCHED,'Order Dispatched'),(ORDER_DELIVERED,'Order Delivered'),(ORDER_CANCELLED,'Order Cancelled'))
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user',null=True,blank=True)
    order_status = models.IntegerField(choices=ORDER_CHOICES,default=ORDER_NOT_PLACED)
    payment_status = models.IntegerField(choices=PAYMENT_CHOICES,default=NOT_PAID)
    delivery_status = models.IntegerField(choices=DELIVERY_CHOICES,default=ORDER_ACCEPTED)
    # transaction_id = models.CharField(max_length=200,null=True)
    order_total_price = models.DecimalField(decimal_places=2,max_digits=20,null=True,blank=True)
    payment_mode = models.CharField(max_length=50,null=True,blank=True)
    delivery_address = models.ForeignKey(ShippingAddress,on_delete=models.SET_NULL,blank=True,null=True)
    create_date = models.DateField(auto_now_add=False,null=True,blank=True)
    delivery_date = models.DateField(auto_now_add=False,null=True,blank=True)
   
    def __str__(self):
        return str(self.id)
    

class OrderItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    quantity =models.IntegerField(default=1,null=True,blank=True)
    item_total_price = models.DecimalField(decimal_places=2,max_digits=20,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True)

# Create your models here.
    @property
    def get_item_total(self):
        total = self.product.product_premium * self.quantity
        return total
    
    def __str__(self):
        return str(self.id)




    # @property
    # def get_total (self):
    #     total = self.product.price * quantity
    #     return total



