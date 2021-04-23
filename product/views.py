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
        return redirect('home')

def add_catagory(request):
    if request.method=='POST':
        name = request.POST['name']
        catagory = Catagory.objects.create(name=name)
        catagory.save()
        return redirect(show_products)
    else:
        return render(request,'add_catagory.html')    


def catagory_items(request,id):
        catagories = Catagory.objects.all()
        catagory = Catagory.objects.get(id=id)
        products= Product.objects.filter(catagory=catagory)
        context = {'products':products,'catagories':catagories}
        return render(request,'userpage.html',context)

def show_catagory(request):
    catagories = Catagory.objects.all()
    return render(request, "catagory.html",{'catagories':catagories})

def edit_catagory(request,id):
    if request.user.is_authenticated and request.method=='POST':
        name = request.POST['name']
        catagory = Catagory.objects.get(id=id)
        catagory.name=name
        catagory.save()

        return redirect(show_catagory)
    catagory = Catagory.objects.get(id=id)
    return render(request, "add_catagory.html",{'catagory':catagory})

def delete_catagory(request,id):
    if request.user.is_authenticated:
        products = Product.objects.filter(catagory=id)
        if products:
            products.delete()
        catagories = Catagory.objects.all()
        return render(request, "catagory.html",{'catagories':catagories})
    else:
        return redirect('home')

def delete_catagory_all(request,id):
    if request.user.is_authenticated:
        products = Product.objects.filter(catagory=id)
        if products:
            products.delete()
        catagory = Catagory.objects.get(id=id)
        if catagory:
            catagory.delete()    
        catagories = Catagory.objects.all()
        return render(request, "catagory.html",{'catagories':catagories})
    else:
        return redirect('home')

def add_product(request):
    if request.method=='POST':
        name = request.POST['name']
        description = request.POST['description']
        product_premium = request.POST['product_premium']
        insure_amount = request.POST['insure_amount']
        # image = request.FILES.get('image')
        image_data = request.POST['pro_img']
        format , imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(base64.b64decode(imgstr), name='temp.'+ ext)

        catagory_id = int(request.POST['catagory_id'])
        catagory = Catagory.objects.get(id=catagory_id)
        
        
        product = Product.objects.create(name=name,catagory=catagory, description=description,product_premium=product_premium,insure_amount=insure_amount,image=data)
        product.save()
        return redirect(show_products)
    else:
        # if request.user.is_superuser:
            
        #     user = User.objects.filter(is_staff=True,is_superuser=False)
        #     return render(request,'admin_add_product.html',{'user':user,'catagories':catagories})
        # else:
        catagories = Catagory.objects.all()
        return render(request,'admin_add_product.html',{'catagories':catagories})

def delete_product(request,id):
    product= Product.objects.get(id=id)
    product.delete()
    return redirect(show_products)


def edit_product(request,id):
    if request.method=='POST':
        name = request.POST['name']
        description = request.POST['description']
        product_premium = request.POST['product_premium']
        insure_amount = request.POST['insure_amount']

        product = Product.objects.get(id=id)
        product.name=name
        product.description=description
        product.product_premium=product_premium
        product.insure_amount=insure_amount
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

    product = Product.objects.get(id=id)
    catagories = Catagory.objects.all()
    if request.user.is_authenticated:  
        return render(request,'loggedin_details_view.html',{'product':product,'catagories':catagories})
    else:
        return render(request,'loggedin_details_view.html',{'product':product,'catagories':catagories})

def view_product_detail(request):
    if request.session['product_id']:
        catagories = Catagory.objects.all()
        product = Product.objects.get(id=request.session['product_id'])
        return render(request,'loggedin_details_view.html',{'product':product,'catagories':catagories})
