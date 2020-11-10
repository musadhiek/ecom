from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from product import views
from django.contrib import messages

# Create your views here.
def logout_request(request):

    auth.logout(request)
    return redirect(home)

def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect(adminpage)
    if  request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
        
            user = auth.authenticate(username=username,password=password)
            if user is not None and user.is_superuser:
                auth.login(request,user)
                return redirect(adminpage)
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
            return redirect(userpage)
        else:
            messages.error(request,'Incorrect username or password')        
            return render(request,'vendor_login.html')    
    else:
        return render(request,'vendor_login.html')   

def user_login(request):
    if request.user.is_authenticated and not request.user.is_staff and not request.user.is_superuser:    
        return redirect(userpage)
    
    if  request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    
        user = auth.authenticate(username=username,password=password)
        if user is not None and not user.is_staff and not user.is_superuser:
            auth.login(request,user)
            return redirect(userpage)
        else:
            messages.error(request,'Incorrect username or password')        
            return render(request,'user_login.html')            
    else:
        return render(request,'user_login.html')

def home(request):
    return render(request,'home.html')

def adminpage(request):
    if request.user.is_authenticated:
        users = User.objects.filter(is_superuser=False,is_staff=True)
        return render(request,'adminpage.html',{'users':users})
    else:
        return redirect(home)

def adminusers(request):
    if request.user.is_authenticated:
        users = User.objects.filter(is_superuser=False,is_staff=False)
        return render(request,'adminpage.html',{'users':users})
    else:
        return redirect(home)        

def userpage(request):
    if request.user.is_authenticated:
        return render(request,'userpage.html')
    else:
        return redirect(home)

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
                return redirect(adminpage)
        else:
             return render(request, 'add_vendor.html',{'warning':'passwords do not match'})      
    return render(request,'add_vendor.html')

def delete_user(request,id):
    user= User.objects.get(id=id)
    user.delete()
    return redirect(adminpage)

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
                return redirect(adminusers)
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