from django.shortcuts import render,redirect
from .models import Product,Catagory
# from purchase.models import Catagory
from django.contrib.auth.models import User,auth 
from PIL import Image
import base64
from django.core.files.base import ContentFile
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

def vendor_add_catagory(request):
    if request.method=='POST':
        name = request.POST['name']
        catagory = Catagory.objects.create(name=name)
        catagory.save()
        return redirect(show_products)
    else:
        return render(request,'vendor_add_catagory.html')    

# def show_catagory_products(request):
#     if request.user.is_authenticated:
#         products= Product.objects.filter()
#         return render(request,'admin_products.html',{'products':products})

def catagory_items(request,id):
        catagories = Catagory.objects.all()
        catagory = Catagory.objects.get(id=id)
        products= Product.objects.filter(catagory=catagory)
        context = {'products':products,'catagories':catagories}
        return render(request,'userpage.html',context)

def add_product(request):
    if request.method=='POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        quantity = request.POST['quantity']
        # image = request.FILES.get('image')
        image_data = request.POST['pro_img']
        format , imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(base64.b64decode(imgstr), name='temp.'+ ext)

        catagory_id = int(request.POST['catagory_id'])
        catagory = Catagory.objects.get(id=catagory_id)
        if request.user.is_superuser:
            vendor_id = int(request.POST['vendor_id'])
            vendor = User.objects.get(id=vendor_id)
        else:    
            vendor= request.user
        product = Product.objects.create(title=title,catagory=catagory, description=description,price=price,quantity=quantity,image=data,vendor=vendor)
        product.save()
        return redirect(show_products)
    else:
        if request.user.is_superuser:
            user = User.objects.filter(is_staff=True,is_superuser=False)
            return render(request,'admin_add_product.html',{'user':user})
        else:
            catagories = Catagory.objects.all()
            return render(request,'vendor_add_product.html',{'catagories':catagories})   

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
    catagories = Catagory.objects.all()
    if request.user.is_authenticated:  
        return render(request,'loggedin_details_view.html',{'product':product,'catagories':catagories})
    else:
        return render(request,'loggedin_details_view.html',{'product':product,'catagories':catagories})