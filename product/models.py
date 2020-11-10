from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(decimal_places=2,max_digits=100,default=1.00)
    quantity = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)
    active = models.BooleanField(default=True)
    vendor= models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    image = models.ImageField(null=True,blank=True)

    @property
    def ImageURL(self):
        try:
            url =self.image.url 
        except:
            url = ''

        return url        