from django.shortcuts import render,redirect
from .models import Product
from django.contrib.auth.models import User,auth 
from PIL import Image
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.contrib.auth import authenticate



# Create your views here.
def show_products(request):
    if request.user.is_superuser:
        products= Product.objects.all()
        return render(request,'admin_products.html',{'products':products})
    else:
        id = request.user.id
        products= Product.objects.filter(vendor_id=id)
        return render(request,'vendor_products.html',{'products':products})

def add_product(request):
    if request.method=='POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        quantity = request.POST['quantity']
        image = request.FILES.get('image')
        if request.user.is_superuser:
            vendor_id = int(request.POST['vendor_id'])
            vendor = User.objects.get(id=vendor_id)
        else:    
            vendor= request.user
        product = Product.objects.create(title=title,description=description,price=price,quantity=quantity,image=image,vendor=vendor)
        product.save()
        return redirect(show_products)
    else:
        if request.user.is_superuser:
            user = User.objects.filter(is_staff=True,is_superuser=False)
            return render(request,'admin_add_product.html',{'user':user})
        else:
            return render(request,'vendor_add_product.html')   

def delete_product(request,id):
    product= Product.objects.get(id=id)
    product.delete()
    return redirect(show_products)


def edit_product(request,id):
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
        if 'image' not in request.POST:
            image = request.FILES.get('image')
        else :
            image=product.image    
        product.image = image
        product.save()
        if request.user.is_staff:
            return redirect(show_products)   
        else:
            return redirect(show_products)
    else:
        product=Product.objects.get(id=id)
        return render(request,'edit_product.html',{'product':product})    

def view_product_details(request,id):
    product = Product.objects.get(id=id)
    if request.user.is_authenticated:  
        return render(request,'loggedin_details_view.html',{'product':product})
    else:
        return render(request,'loggedout_details_view.html',{'product':product})