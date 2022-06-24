from calendar import c
from django import forms
 

class LoginForm(forms.Form):
    name = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)
    firstname = forms.CharField(max_length=20)
    lastname = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)
    password_confirmation = forms.CharField(max_length=20)
    email=forms.EmailField(max_length=50)
    phone=forms.IntegerField()
    facebookurl=forms.URLField(max_length=50)
    country=forms.CharField(max_length=20)
    birthday=forms.DateField()
    img = forms.ImageField()



