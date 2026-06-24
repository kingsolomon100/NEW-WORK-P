from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required 
from django.contrib import messages 
from django.contrib.auth import login, logout 
from django.contrib.auth.forms import AuthenticationForm
from .models import Product 
from .forms import UserRegistrationForm, ProductUserForm 

@login_required
def product_list_view(request):
    products = Product.objects.filter(user= request.user).order_by('-product_id')
    return render(request, 'accounts/product_list.html', {'products': products})

@login_required
def product_create_view(request):
    if request.method == 'POST':
        form = ProductUserForm(request.POST) 
        if form.is_valid():
            cleaned_data = form.cleaned_data 
            sku = cleaned_data.get('sku')
            quantity_to_add = cleaned_data.get('quantity', 0)

            defaults_dict = {
                'name': cleaned_data.get('name'), 
                'price': cleaned_data.get('price'), 
                'supplier': cleaned_data.get('supplier')
            }

            product = Product.add_or_update_product(
                user= request.user,
                sku= sku, 
                quantity_to_add= quantity_to_add, 
                defaults_dict= defaults_dict
            )
            messages.success(request, f"✅ Product {product.name} is processed successfully. Current Stock: {product.quantity}")
            return redirect('product_list')
        return product 
    else:
        form = ProductUserForm()
    return render(request, 'accounts/product_create.html', {'form': form})    

@login_required
def product_update_view(request, product_id):
    product = get_object_or_404(Product, product_id=product_id, user=request.user) 
    if request.method == 'POST':
        form = ProductUserForm(request.POST, instance=product) 
        if form.is_valid():
            form.save()
            messages.success(request, f"👍{product.name} has been updated successfully")
            return redirect('product_list')
        else:
            messages.error(request, "Failed Update due to incorrect Id")

    else:
        form = ProductUserForm(instance=product)
    return render(request, 'accounts/product_update.html', {'form': form,  'product': product   })

@login_required
def product_delete_view(request, product_id):
    product = get_object_or_404(Product, product_id=product_id, user=request.user)
    if request.method == 'POST':
        product.delete()
        messages.info(request, f"{product.name} has been deleted")
        return redirect('product_list')
    return render(request, 'accounts/product_confirm_delete.html', {'product': product})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"✅ Weldone, Registration completed by {user.username}")
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request): 
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST': 
        logout(request)
        return redirect('login')
    return render(request, 'accounts/logout.html')   

def home_view(request):
    return render(request, 'accounts/home.html')             



