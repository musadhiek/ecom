from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.db import models
from product.models import Product,Catagory
from .models import OrderItem,Order,ShippingAddress
import datetime
import json
from django.http import JsonResponse
#error with csrf cooki in payment
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def show_cart(request):
    if request.user.is_authenticated:
        user =request.user 
        catagories = Catagory.objects.all()
        order, created = Order.objects.get_or_create(user=user,order_status=Order.ORDER_NOT_PLACED)
        items = order.orderitem_set.all()
        count = items.count()
        
        total = 0
        for item in items:
            total += item.quantity * item.product.product_premium
            item.item_total_price = item.get_item_total
        if count ==0:
            message = "There is no items in Your cart!" 
            return render(request,'user_cart.html',{'items':items,'message':message})
        context ={'items':items,'count':count,'total':total,'catagories':catagories}    
        return render(request,'user_cart.html',context)
    else:
        return redirect(home)    

def add_to_cart(request,id):
        if request.user.is_authenticated:
            
            product = Product.objects.get(id=id)
            user = request.user
            order, created = Order.objects.get_or_create(user=user,order_status=Order.ORDER_NOT_PLACED)
            if OrderItem.objects.filter(user=user,order=order,product=product).exists():
                item =OrderItem.objects.get(user=user,order=order,product=product) 
                item.quantity = item.quantity+1
                item.item_total_price = item.quantity * item.product.product_premium    
                item.save()
                return redirect('home')
                
            else:

                item = OrderItem.objects.create( user=user,order=order,product=product)
                item.item_total_price = item.quantity * item.product.product_premium
                item.save()
                return redirect('home')
        else:
            request.session['product_id']=id
            return redirect('user_login')

def delete_cart_item(request,id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        order= Order.objects.get(user=request.user,order_status=Order.ORDER_NOT_PLACED)
        item = OrderItem.objects.get(product=product,user=request.user,order=order)
        item.delete()
        return redirect(show_cart)
    else:
        return redirect('home')    

def add_one_quantity(request,id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        order = Order.objects.get(user=request.user,order_status=Order.ORDER_NOT_PLACED)
        item = OrderItem.objects.get(product=product,user=request.user,order=order)
        item.quantity +=1
        item.item_total_price = item.product.product_premium * item.quantity
        item.save()
        return redirect(show_cart)
    else:
        return redirect('home')    

def remove_one_quantity(request,id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        order = Order.objects.get(user=request.user,order_status=Order.ORDER_NOT_PLACED)
        item = OrderItem.objects.get(product=product,user=request.user,order=order)
        if item.quantity>1:
            item.quantity -=1
            item.item_total_price = item.product.product_premium * item.quantity
            item.save()
            return redirect(show_cart)
        else :
            item.delete()
            return redirect(show_cart)   
        
    else:
        return redirect('home')    
    

def confirm_purchase(request):
    if request.user.is_authenticated:
        order, create = Order.objects.get_or_create(user=request.user,order_status=Order.ORDER_NOT_PLACED)
        if request.method == 'POST' :
            payment_mode = request.POST['payment']
            if payment_mode == 'COD':
               
                order.order_status = Order.ORDER_PLACED
                order.payment_mode = 'COD'
                order.create_date=datetime.date.today()
                order.save()
                return JsonResponse('Order Placed',safe=False)
            
        
           
        items = order.orderitem_set.all()
        order.order_total_price = 0
        count = items.count()
        if ShippingAddress.objects.filter(user=request.user,default_address=True).exists():
            delivery_address =ShippingAddress.objects.get(user=request.user,default_address=True)
            if count >1:
                for item in items:
                    order.order_total_price += item.item_total_price
            else:
                item = OrderItem.objects.get(order=order)
                order.order_total_price = item.item_total_price
            
            # order.create_date = datetime.today()
            
            order.save()
            total = order.order_total_price
            context = {'count':count,'total':total,'delivery_address':delivery_address,'items':items}
            return render(request,'confirm_purchase.html',context)
        else:
            return render(request,'confirm_purchase.html')
    else:
        return redirect('home')
    
def process_order(request):

    print("process root")
    if request.method == 'POST':
    # transaction_id = datetime.datetime.now().timestamp()
        data = json.loads(request.body)
        print('hello', data)

        if request.user.is_authenticated:
            user = request.user
            order, created = Order.objects.get_or_create(user=user,order_status=Order.ORDER_NOT_PLACED)
            total = float(data['form']['total'])
            # order.transaction_id = transaction_id

            # if total == order.order_total_price:
            order.order_status = Order.ORDER_PLACED
            order.payment_status = Order.PAID
            order.payment_mode = 'PAYPAL'
            order.create_date=datetime.date.today()
            order.save() 
           
            return JsonResponse(safe=False)
    
            # 
        else:
            print('user not logged in')
            return JsonResponse(safe=False)
    else:
        return JsonResponse(safe=False)

def accept_order(request,id):
    if request.user.is_superuser:
        order = Order.objects.get(id=id)
        order.delivery_status = Order.ORDER_DISPATCHED
        order.save()
        return redirect('admin_order_history')
    else:
        return redirect('home')    

def reject_order(request,id):
    if request.user.is_superuser:
        order = Order.objects.get(id=id)
        order.delivery_status = Order.ORDER_CANCELLED
        order.save()
        return redirect('admin_order_history')
    else:
        return redirect('home')    
        
           

def order_history(request):
    if request.user.is_authenticated:
        user =request.user
        catagories = Catagory.objects.all()
        orders = Order.objects.filter(user=user,order_status=Order.ORDER_PLACED)
        dict = {}
        for order in orders:
            dict[order]=OrderItem.objects.filter(user=request.user,order=order)
        context ={'dict':dict,'catagories':catagories}
        return render(request,'user_order_history.html',context)
    else:
        return redirect('home')  

def admin_order_history(request):
    if request.user.is_authenticated:
        
        orders = Order.objects.filter(order_status=Order.ORDER_PLACED)
        dict = {}
        for order in orders:
            dict[order]= OrderItem.objects.filter(order=order)
        context ={'dict':dict}
        return render(request,'admin_order_history.html',context)
    else:
        return redirect('admin_vendor_page')  

def admin_order_delete(request,id):
    if request.user.is_authenticated:
        orders = Order.objects.filter(id=id)
        orders.delete()
        return redirect(admin_order_history)
    else:
        return redirect('home')



def add_shipping_address(request):
    print('yes')
    if request.user.is_authenticated:
        return render(request,'add_shipping_address.html') 
    else:
        return redirect('home')

def save_address(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        postal_code = request.POST['postal_code']
        if ShippingAddress.objects.filter(user=request.user,default_address=True).count() == 0:
            shipping_address=ShippingAddress.objects.create(user=request.user ,phone=phone,address=address,city=city,state=state,pincode=postal_code,default_address=True)
            shipping_address.save()
            return redirect('user_profile')
        else:
            shipping_address=ShippingAddress.objects.create(user=request.user ,phone=phone,address=address,city=city,state=state,pincode=postal_code)
            shipping_address.save()
            return redirect('user_profile')
    else:
        return redirect('user_profile')


def delete_address(request,id):
    if request.user.is_authenticated:
        address = ShippingAddress.objects.get(user=request.user,id=id)
        address.delete()
        return redirect('user_profile')
    else:
        return redirect('home')

def change_address(request):
    if request.user.is_authenticated:
        return redirect('user_profile')
    else:
        return redirect('home')

def make_primary(request,id):
    if request.user.is_authenticated:
        other_address = ShippingAddress.objects.filter(user=request.user)
        for address in other_address:
            address.default_address=False
            address.save()
        if ShippingAddress.objects.filter(user=request.user,id=id).exists():
            primary_address = ShippingAddress.objects.get(user=request.user,id=id)
            primary_address.default_address =True  
            primary_address.save()
            return redirect('user_profile')
        else:
            return redirect('user_profile')  
    else:
        return redirect('home')            