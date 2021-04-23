from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from product import views
from django.db import models
from django.contrib import messages
from product.models import Product, Catagory
from purchase.models import OrderItem, Order, ShippingAddress
from .models import UserProfile
from PIL import Image
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import requests
import json
import datetime
import calendar

from django.db.models import Count, Sum
# Create your views here.


def logout_request(request):

    auth.logout(request)
    return redirect(home)


def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect(admin_dashboard)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            auth.login(request, user)
            return redirect(admin_dashboard)
        else:
            messages.error(request, 'Incorrect username or password')
            return render(request, 'admin_login.html',)
    else:
        return render(request, 'admin_login.html')




def user_login(request):
    if request.user.is_authenticated and request.user.is_active  and not request.user.is_superuser:
        return redirect(userpage)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None and not user.is_staff and user.is_active and not user.is_superuser:
            auth.login(request, user)
            if 'product_id' in request.session:
                id = request.session['product_id']
                return redirect("view_product_detail")
            else:
                return redirect(userpage)
        else:
            messages.error(request, 'Incorrect username or password')
            return render(request, 'user_login.html')
    else:
        return render(request, 'user_login.html')


def login_with_otp(request):
    return render(request, "login_with_otp.html")


def enter_otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        otp_id = request.session['otp_id']
        customer_id = request.session['customer_id']
        user = User.objects.get(id = customer_id)
        url = "https://d7networks.com/api/verifier/verify"

        payload = {'otp_id': otp_id,
                   'otp_code': otp}
        files = [

        ]
        headers = {
            'Authorization': 'Token 8df27b0ad9bd2c2e8112f5dad4db5b4d55115e95'
        }

        response = requests.request(
            "POST", url, headers=headers, data=payload, files=files)

        data = response.text.encode('utf8')
        dict = json.loads(data.decode('utf8'))
        status = dict['status']
        if status == 'success':

            auth.login(request,user)
            return redirect(home)
        else:
            return redirect(home)
    else:
        return render(request, 'enter_otp.html')


def send_otp(request):
    if request.method == 'POST':
        mobile = request.POST['mobile']

        if UserProfile.objects.filter(mobile=mobile).exists():
            user_profile = UserProfile.objects.get(mobile=mobile)
            customer = User.objects.get(id=user_profile.user.id)
            mobile = str(91)+mobile
            if customer.is_active:
                url = "https://d7networks.com/api/verifier/send"
                payload = {'mobile': mobile,
                           'sender_id': 'SMSINFO',
                           'message': 'Your otp code is {code}',
                           'expiry': '9000'}
                files = [
                ]
                headers = {
                    'Authorization': 'Token 8df27b0ad9bd2c2e8112f5dad4db5b4d55115e95'
                }
                response = requests.request(
                    "POST", url, headers=headers, data=payload, files=files)
                data = response.text.encode('utf8')
                dict = json.loads(data.decode('utf8'))
                otp_id = dict['otp_id']
                request.session['otp_id'] = otp_id
                request.session['customer_id']=customer.id
                return redirect(enter_otp)
            else:
                return redirect(home,)
        else:
            return redirect(login_with_otp)


def home(request):
    products = Product.objects.all()
    catagories = Catagory.objects.all()
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, order_status=Order.ORDER_NOT_PLACED)
        count = order.orderitem_set.all().count()

        context = {'products': products,
                   'count': count, 'catagories': catagories}
        return render(request, 'userpage.html', context)
    else:
        context = {'products': products, 'catagories': catagories}
        return render(request, 'home.html', context)


def admin_dashboard(request):
    if request.user.is_authenticated:
        date = datetime.date.today()
        orders = Order.objects.filter(create_date=date)
        user = []
        sale = 0
        user_count = 0
        product_count = 0
        order_count = 0
        for order in orders:
            sale += order.order_total_price
            if order.user not in user:
                user_count += 1
                user.append(order.user)
            for orderitem in OrderItem.objects.filter(order=order):
                product_count += orderitem.quantity
            order_count += 1

        context = {'user_count': user_count, 'product_count': product_count,
                   'order_count': order_count, 'date': date, 'sale': sale}

    return render(request, "admin_dashboard.html", context)


def admin_sale_report(request):
    if request.user.is_authenticated and request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        data = Order.objects.filter(create_date__range=[start_date, end_date]).values('create_date').annotate(
            user_count=Count('user_id'), total_order=Count('id'), amount=Sum('order_total_price')).order_by('-create_date')
        return render(request, "admin_sale_report.html", {'data': data})
    else:
        end_date = datetime.date.today()
        start_date = datetime.date.today().replace(day=1)
        data = Order.objects.filter(create_date__range=[start_date, end_date]).values('create_date').annotate(
            user_count=Count('user_id'), total_order=Count('id'), amount=Sum('order_total_price')).order_by('-create_date')
        return render(request, "admin_sale_report.html", {'data': data})

def admin_cancelled_report(request):
    if request.user.is_authenticated and request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        data = Order.objects.filter(create_date__range=[start_date, end_date],delivery_status=Order.ORDER_CANCELLED).values('create_date').annotate(
            user_count=Count('user_id'), total_order=Count('id'), amount=Sum('order_total_price')).order_by('-create_date')
       
        return render(request, "admin_cancelled_report.html", {'data': data})
    else:
        end_date = datetime.date.today()
        start_date = datetime.date.today().replace(day=1)
        data = Order.objects.filter(create_date__range=[start_date, end_date],delivery_status=Order.ORDER_CANCELLED).values('create_date').annotate(
            user_count=Count('user_id'), total_order=Count('id'), amount=Sum('order_total_price')).order_by('-create_date')
        return render(request, "admin_cancelled_report.html", {'data': data})

def admin_monthly_report(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            date = request.POST['start_date']
            dt = datetime.datetime.strptime(date, '%Y-%m-%d')
            month = dt.month
            data = Order.objects.filter(create_date__month=month).values('create_date').annotate(user_count=Count(
                'user_id'), total_order=Count('id'), amount=Sum('order_total_price')).order_by('-create_date')
            return render(request, "admin_monthly_report.html", {'data': data})

        else:
            start_date = datetime.date.today().replace(day=1)
            end_date = datetime.date.today()
            data = Order.objects.filter(create_date__range=[start_date, end_date]).values('create_date').annotate(
                user_count=Count('user_id'), total_order=Count('id'), amount=Sum('order_total_price')).order_by('-create_date')
            return render(request, "admin_monthly_report.html", {'data': data})
    return redirect(home)


def admin_vendor_page(request):
    if request.user.is_authenticated:
        users = User.objects.filter(is_superuser=False, is_staff=True)
        return render(request, 'admin_vendor_page.html', {'users': users})
    else:
        return redirect(home)


def admin_user_page(request):
    if request.user.is_authenticated:
        users = User.objects.filter(is_superuser=False, is_staff=False)
        return render(request, 'admin_user_page.html', {'users': users})
    else:
        return redirect(home)


def userpage(request):
    if request.user.is_authenticated:
        catagories = Catagory.objects.all()
        products = Product.objects.all()
        order, create = Order.objects.get_or_create(
            user=request.user, order_status=Order.ORDER_NOT_PLACED)
        count = OrderItem.objects.filter(
            user=request.user, order=order).count()

        return render(request, 'userpage.html', {'products': products, 'count': count, 'catagories': catagories})
    else:
        return redirect(home)

#Genarating user profile
def user_profile(request):
    if request.user.is_authenticated:
        shipping_address = ShippingAddress.objects.filter(
            user=request.user, default_address=False)
        # if ShippingAddress.objects.filter(user=request.user, default_address=True).exists():
        primary_address = ShippingAddress.objects.filter(
                user=request.user, default_address=True).exists()
                    
        if UserProfile.objects.filter(user=request.user).exists():
            profile = UserProfile.objects.get(user=request.user)
            context = {'shipping_address': shipping_address,
                       'primary_address': primary_address, 'profile': profile}
            return render(request, 'user_profile.html', context)
        else:
            context = {'shipping_address': shipping_address,
                       'primary_address': primary_address}
            return render(request, 'user_profile.html', context)
    else:
        return redirect(home)


def edit_user_profile(request):
    profile, create = UserProfile.objects.get_or_create(user=request.user)
    if request.user.is_authenticated and request.method == 'POST':
        name = request.POST['name']
        mobile = request.POST['mobile']
        occupation = request.POST['occupation']
        location = request.POST['location']
        image_data = request.POST['pro_img']
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        profile.name = name
        profile.mobile = mobile
        profile.occupation = occupation
        profile.location = location
        profile.profile_picture = data
        profile.save()
        return redirect(user_profile)
    return render(request, "edit_user_profile.html", {'profile': profile})


def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect(admin_user_page)


def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['password2']
        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.error(request,'a user with this email already exists')
                return render(request, 'user_signup.html')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password, is_staff=False, is_superuser=False)
                user.save()
                auth.login(request, user)
                return render(request, 'userpage.html')
        else:
            return render(request, 'user_signup.html', {'warning': 'passwords do not match'})
        return(request, 'user_signup.html')
    return render(request, 'user_signup.html')


def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['password2']
        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                return render(request, 'add_user.html', {'warning': 'a user with this email already exists'})
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password, is_staff=False, is_superuser=False)
                user.save()
                return redirect(admin_user_page)
        else:
            return render(request, 'add_user.html', {'warning': 'passwords do not match'})
    return render(request, 'add_user.html')


def edit_user(request, id):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        user = User.objects.get(id=id)
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken')
            return render(request, 'edit_user.html', {'user': user})
        else:
            user = User.objects.get(id=id)
            user.username = username
            user.email = email
            user.save()
            return redirect(adminpage)
    user = User.objects.get(id=id)
    return render(request, 'edit_user.html', {'user': user})


def block_user(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        user = User.objects.get(id=id)
        user.is_active = False
        user.save()
        return redirect(admin_user_page)
    else:
        return redirect(home)


def unblock_user(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        user = User.objects.get(id=id)
        user.is_active = True
        user.save()
        return redirect(admin_user_page)
    else:
        return redirect(home)
