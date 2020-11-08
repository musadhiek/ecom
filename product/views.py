from django.shortcuts import render,redirect
from .models import Product
from django.contrib.auth.models import User,auth 

# Create your views here.
def show_products(request):
    products= Product.objects.all()
    return render(request,'admin_products.html',{'products':products})

def add_product(request):
    if request.method=='POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        quantity = request.POST['quantity']
        
        product = Product.objects.create(title=title,description=description,price=price,quantity=quantity)
        product.save()
        return redirect(show_products)
    vendor = User.objects.filter(is_staff=True,is_superuser=False)    
    return render(request,'add_product.html',{'vendor':vendor})   

def delete_product(request,id):
    product= Product.objects.get(id=id)
    product.delete()
    return redirect(show_products)

def edit_product(request,id):
    product=Product.objects.get(id=id)
    return render(request,'edit_product.html',{'product':product})

def edited_product(request,id):
    if request.method=='POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        quantity = request.POST['quantity']
        
        product = Product.objects.get(id=id)
        product.title=title
        product.description=description
        product.price=price
        product.quantity=quantity
        product.save()
        return redirect(show_products)
    else:
        return redirect(show_products)