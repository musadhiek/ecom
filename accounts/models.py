from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):

    name = models.CharField(max_length=100,blank=True,null=True)
    profile_picture = models.ImageField(blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    occupation = models.CharField(max_length=100,blank=True,null=True)
    location = models.CharField(max_length=200,blank=True,null=True)

    @property
    def ImageURL(self):
        try:
            url = self.profile_picture.url
        except:
            url = ''
        return url        

    def __str__(self):
        return (self.name)

