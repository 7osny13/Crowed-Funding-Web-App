from calendar import c
from contextlib import nullcontext
from pydoc import describe
from re import T
from unicodedata import name
from django.db import models
from django_countries.fields import CountryField





class UserProfile(models.Model):
    user_id= models.BigIntegerField(default=None)
    user_img= models.ImageField(null=True, blank=True,upload_to='img/')
    # user_type= models.CharField(max_length=20,default=None)
    user_phone=models.IntegerField()
    user_facebook=models.CharField(max_length=200)
    user_country= CountryField()
    user_birthday=models.DateField() 
    # def __str__(self):
    #     return self.name