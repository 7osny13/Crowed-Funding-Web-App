from calendar import c
from contextlib import nullcontext
from pydoc import describe
from re import T
from unicodedata import name
from django.db import models
 




class UserProfile(models.Model):
    user_id= models.IntegerField(default=None)
    user_img= models.ImageField(null=True, blank=True,upload_to='img/')
    user_phone=models.IntegerField()
    user_facebook=models.CharField(max_length=200)
    user_country= models.CharField(max_length=50)
    user_birthday=models.DateField(null=True, blank=True) 
    def __str__(self):
        return self.name