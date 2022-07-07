from calendar import c
import datetime
from django import forms
from matplotlib import widgets 
from django.contrib.auth.models import User
from django_countries.fields import CountryField
import validate_email as ve



class LoginForm(forms.Form):
    name = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)

# class DateInput(forms.DateInput):
#     input_type = 'date'
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)

    firstname = forms.CharField(max_length=20)
    lastname = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20,widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=20,widget=forms.PasswordInput)
    email=forms.EmailField(max_length=50)
    # user_type = forms.ChoiceField(choices=[('owner', 'Owner'), ('doner', 'Doner')])
    user_phone=forms.IntegerField()
    user_facebook=forms.URLField(max_length=50)
    user_country=CountryField().formfield()
    user_birthday=forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    # user_img = forms.ImageField()
    def clean_username(self):
        username = self.cleaned_data.get("username")
    
        if len(username) < 8:
            # raise messages.error(request, 'Document deleted.')

            raise forms.ValidationError("username must be at least 8 characters" )
        if User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError("This username is already exists" )
        uouo=username.isnumeric()
        if uouo:
            raise forms.ValidationError("username can not be numbers" )
        
        
        
        return username
    def clean_password_confirmation(self):
        password = self.cleaned_data.get("password")
        password_confirmation = self.cleaned_data.get("password_confirmation")
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters" )
        pass1=str(password)
        pass2=str(password_confirmation)
        if pass1!=pass2:
            raise forms.ValidationError("password and password confirmation not match" )
       
        return password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # if ve.validate_email(email)==False:
            
        #     raise forms.ValidationError("Email is not valid" )
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError("This email is already exists" )
        
        return email
    def clean_user_phone(self):
        user_phone = self.cleaned_data.get("user_phone")
        if len(str(user_phone)) < 12:
            raise forms.ValidationError("Phone number must be at least 12 digits" )
        user_phone1= str(user_phone)
        if not user_phone1.startswith('20'):
            raise forms.ValidationError("Phone number must start with '20' as Egyptian number" )

        return user_phone
    def clean_user_birthday(self):
        user_birthday = self.cleaned_data.get("user_birthday")
        
        if user_birthday > datetime.date.today():
            raise forms.ValidationError("Birthday can not be future date" )
        return user_birthday
    def clean_user_country(self):
        user_country = self.cleaned_data.get("user_country")
        if user_country != 'EG':
            raise forms.ValidationError("you must choose Egypt" )
        # if user_country != "Egypt":
        #     raise forms.ValidationError("you must choose Egypt" )
        return user_country
    # def clean_user_img(self):
    #     user_img = self.cleaned_data.get("user_img")
    #     if user_img == None:
    #         raise forms.ValidationError("you must choose image" )
    #     return user_img
    username.widget.attrs['class'] = 'form-control'
    firstname.widget.attrs['class'] = 'form-control'
    lastname.widget.attrs['class'] = 'form-control'
    password.widget.attrs['class'] = 'form-control'
    password_confirmation.widget.attrs['class'] = 'form-control'
    email.widget.attrs['class'] = 'form-control'
    user_phone.widget.attrs['class'] = 'form-control'
    user_facebook.widget.attrs['class'] = 'form-control'
    user_country.widget.attrs['class'] = 'form-control'
    user_birthday.widget.attrs['class'] = 'form-control'
   