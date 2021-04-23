from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from .models import *

# Create your models here.
class Catagory(models.Model):
    name = models.CharField(max_length=200,null=True)

    def __str__(self):
       return(self.name)

class Product(models.Model):
    name = models.CharField(max_length=120)
    catagory = models.ForeignKey(Catagory,on_delete=models.CASCADE,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    product_premium = models.DecimalField(decimal_places=2,max_digits=100,default=1.00)
    insure_amount = models.DecimalField(decimal_places=2,max_digits=100,default=1.00)
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)
    active = models.BooleanField(default=True)
    # vendor= models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    image = models.ImageField(null=True,blank=True)

    @property
    def ImageURL(self):
        try:
            url =self.image.url 
        except:
            url = ''

        return url        

    def __str__(self):
       return(self.title)