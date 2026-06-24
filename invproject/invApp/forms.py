from django import forms 
from django.contrib.auth import get_user_model 
from .models import Product 

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput)
    confirm_password = forms.CharField(widget= forms.PasswordInput)

    class Meta:
        model = User 
        fields = ['email', 'username']

    def clean(self): 
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
             self.add_error('confirm_password', 'Password do not match')
        return cleaned_data 

    def save(self, commit= True):
        user = super().save(commit= False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user 

class ProductUserForm(forms.ModelForm): 
    class Meta:
        model = Product
        fields = ['name', 'sku', 'price', 'quantity', 'supplier']

        labels = {
            'name': 'Product Name', 
            'sku':  'Barcode/SKU', 
            'price':  'Price of product', 
            'quantity': 'Quantity of goods', 
            'supplier':  'Vendor/Supplier'
        }

    widgets = {
        'name':  forms.TextInput, 
        'sku':   forms.TextInput,
        'price':  forms.NumberInput, 
        'quantity': forms.NumberInput, 
        'supplier':  forms.TextInput    
    } 


