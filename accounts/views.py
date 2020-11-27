from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from product import views
from django.db import models
from django.contrib import messages
from product.models import Product, Catagory
from purchase.models import OrderItem,Order,ShippingAddress
from .models import UserProfile
from PIL import Image
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.files import File

# Create your views here.
def logout_request(request):

    auth.logout(request)
    return redirect(home)

def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect(admin_dashboard)
    if  request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
        
            user = auth.authenticate(username=username,password=password)
            if user is not None and user.is_superuser:
                auth.login(request,user)
                return redirect(admin_dashboard)
            else:
                messages.error(request,'Incorrect username or password')        
                return render(request,'admin_login.html',)
    else:
        return render(request,'admin_login.html')

def vendor_login(request):
    if request.user.is_authenticated and request.user.is_staff and not request.user.is_superuser:    
        return redirect(vendorpage)
    
    if  request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)
        if user is not None and user.is_staff and not user.is_superuser:
            auth.login(request,user)
            return redirect(vendorpage)
        else:
            messages.error(request,'Incorrect username or password')        
            return render(request,'vendor_login.html')    
    else:
        return render(request,'vendor_login.html')   

def user_login(request):
    if request.user.is_authenticated and user.is_active and not request.user.is_staff and not request.user.is_superuser:    
        return redirect(userpage)
    
    if  request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    
        user = auth.authenticate(username=username,password=password)
        if user is not None and not user.is_staff and user.is_active and not user.is_superuser:
            auth.login(request,user)
            return redirect(userpage)
        else:
            messages.error(request,'Incorrect username or password')        
            return render(request,'user_login.html')            
    else:
        return render(request,'user_login.html')

def home(request):
    products = Product.objects.all()
    catagories = Catagory.objects.all()
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user,order_status=Order.ORDER_NOT_PLACED)
        count = order.orderitem_set.all().count()
        
        context = {'products':products,'count':count,'catagories':catagories}
        return render(request,'userpage.html',context)
    else:
        context = {'products':products,'catagories':catagories}
        return render(request,'home.html',context)

def admin_dashboard(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(create_date__range=('2020-11-15','2020-11-23'))
        print(orders)
        user = []
        product = 0
        order_count = 0
        for order in orders:
            if order.user not in user:
                print(order.user)
                user.append(order.user)
            for orderitem in OrderItem.objects.filter(order=order):
                print(orderitem.quantity)
            order_count +=1
        
        context={'users':len(user),'product':product,'order_count':order_count}           

    return render(request,"admin_dashboard.html",context)
def admin_vendor_page(request):
    if request.user.is_authenticated:
        users = User.objects.filter(is_superuser=False,is_staff=True)
        return render(request,'admin_vendor_page.html',{'users':users})
    else:
        return redirect(home)

def admin_user_page(request):
    if request.user.is_authenticated:
        users = User.objects.filter(is_superuser=False,is_staff=False)
        return render(request,'admin_user_page.html',{'users':users})
    else:
        return redirect(home)        

def admin_order_page(request):
    if request.user.is_authenticated:
        users = User.objects.filter(is_superuser=False,is_staff=False)
        orders = Order.objects.all()
        return render(request,'admin_order_history.html',{'orders':orders})
    else:
        return redirect(home)  

def userpage(request):
    if request.user.is_authenticated:
        catagories = Catagory.objects.all()
        products =Product.objects.all()
        order,create = Order.objects.get_or_create(user=request.user,order_status=Order.ORDER_NOT_PLACED)
        count = OrderItem.objects.filter(user=request.user,order=order).count()
        
        return render(request,'userpage.html',{'products':products,'count':count,'catagories':catagories})
    else:
        return redirect(home)

def user_profile(request):
    if request.user.is_authenticated:
        shipping_address = ShippingAddress.objects.filter(user=request.user,default_address=False)
        if ShippingAddress.objects.filter(user=request.user,default_address=True).exists():
            primary_address = ShippingAddress.objects.get(user=request.user,default_address=True)
        if UserProfile.objects.filter(user=request.user).exists():
            print("its working")
            profile =  UserProfile.objects.get(user=request.user)
            context = {'shipping_address':shipping_address,'primary_address':primary_address,'profile':profile}
            return render(request,'user_profile.html',context)
        else:
            context = {'shipping_address':shipping_address,'primary_address':primary_address}
            return render(request,'user_profile.html',context)
    else:
        return redirect(home)
def edit_user_profile(request):
    if request.user.is_authenticated and request.method == 'POST':
        name =  request.POST['name']
        occupation =  request.POST['occupation']
        location =  request.POST['location']
        image_data = request.POST['pro_img']
        format , imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name='temp.'+ ext)

        profile, create = UserProfile.objects.get_or_create(user= request.user)
        profile.name=name
        profile.occupation=occupation
        profile.location= location
        profile.profile_picture = data
        profile.save()

        return redirect(user_profile)
    
    return render(request,"edit_user_profile.html")
def vendorpage(request):
    if request.user.is_authenticated:
        return redirect(views.show_products)
    else:
        return redirect(home)

def vendor_signup(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['password2']
        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                return render(request, 'vendor_signup.html',{'warning':'a user with this email already exists'})
            else:
                user =User.objects.create_user(password=password,email=email,username=username, is_staff=True,is_superuser=False)
                user.save()
                auth.login(request,user)
                return render(request,'vendorpage.html')
        else:
             return render(request, 'vendor_signup.html',{'warning':'passwords do not match'})     
        return(request,'vendor_signup.html')       
    return render(request,'vendor_signup.html')

def add_vendor(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['password2']
        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                return render(request, 'add_vendor.html',{'warning':'a user with this email already exists'})
            elif User.objects.filter(username=username).exists():
                return render(request, 'add_vendor.html',{'warning':'this username is taken'})
            else:
                user =User.objects.create_user(username=username,email=email,password=password,is_staff=True,is_superuser=False)
                user.save()
                users = User.objects.filter(is_superuser=False)
                return redirect(admin_vendor_page)
        else:
             return render(request, 'add_vendor.html',{'warning':'passwords do not match'})      
    return render(request,'add_vendor.html')

def delete_user(request,id):
    user= User.objects.get(id=id)
    user.delete()
    return redirect(admin_vendor_page)

def user_signup(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['password2']
        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                return render(request, 'user_signup.html',{'warning':'a user with this email already exists'})
            else:
                user =User.objects.create_user(username=username,email=email,password=password,is_staff=False,is_superuser=False)
                user.save()
                auth.login(request,user)
                return render(request,'userpage.html')
        else:
             return render(request, 'user_signup.html',{'warning':'passwords do not match'})     
        return(request,'user_signup.html')       
    return render(request,'user_signup.html')

def add_user(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['password2']
        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                return render(request, 'add_user.html',{'warning':'a user with this email already exists'})
            else:
                user =User.objects.create_user(username=username,email=email,password=password,is_staff=False,is_superuser=False)
                user.save()
                return redirect(admin_user_page)
        else:
             return render(request, 'add_user.html',{'warning':'passwords do not match'})      
    return render(request,'add_user.html')

def edit_user(request,id):

    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        user = User.objects.get(id=id)
        if User.objects.filter(email=email).exists():
            messages.error(request,'Email already taken')
            return render(request,'edit_user.html',{'user':user})
        else:
            user = User.objects.get(id=id)
            user.username=username
            user.email=email
            user.save()
            return redirect(adminpage)
    user = User.objects.get(id=id)
    return render(request,'edit_user.html',{'user':user})     

def block_user(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        user  = User.objects.get(id=id)
        user.is_active = False
        user.save()
        return redirect(admin_user_page)
    else:
        return redirect(home)

def unblock_user(request,id):
    if request.user.is_authenticated and request.user.is_superuser :
        user  = User.objects.get(id=id)
        user.is_active = True
        user.save()
        return redirect(admin_user_page)
    else:
        return redirect(home)




