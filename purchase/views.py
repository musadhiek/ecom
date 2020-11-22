from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.db import models
from product.models import Product,Catagory
from .models import OrderItem,Order,ShippingAddress
import uuid

# Create your views here.

def show_cart(request):
    if request.user.is_authenticated:
        user =request.user 
        catagories = Catagory.objects.all()
        items = OrderItem.objects.filter(user=user)
        orders = Order.objects.filter(user=user)
        count = items.count()
        total = 0
        for item in items:
            total += item.price
        if count ==0:
            message = "There is no items in Your cart!" 
            return render(request,'user_cart.html',{'items':items,'message':message})
        context ={'items':items,'orders':orders,'count':count,'total':total,'catagories':catagories}    
        return render(request,'user_cart.html',context)
    else:
        return redirect(home)    

def add_to_cart(request,id):
        if request.user.is_authenticated:
            
            product = Product.objects.get(id=id)
            user = request.user
            if OrderItem.objects.filter(product=product).exists():
                item =OrderItem.objects.get(product=product) 
                if item.quantity <= item.product.quantity:
                    item.quantity = item.quantity+1
                    item.price = item.quantity*item.product.price
                    item.save()
                    return redirect('home')
                else:
                    return redirect('home')
            else:

                orderitem = OrderItem.objects.create( user=user, product=product,price=product.price)
                orderitem.save()
                return redirect('home')
        else:
            return redirect('home')

def delete_cart_item(request,id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        item = OrderItem.objects.get(product=product,user=request.user)
        item.delete()
        return redirect(show_cart)
    else:
        return redirect('home')    
def add_one_quantity(request,id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        item = OrderItem.objects.get(product=product,user=request.user)
        item.quantity +=1
        item.price = item.product.price * item.quantity
        item.save()
        return redirect(show_cart)
    else:
        return redirect('home')    

def remove_one_quantity(request,id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        item = OrderItem.objects.get(product=product,user=request.user)
        if item.quantity>1:
            item.quantity -=1
            item.price = item.product.price * item.quantity
            item.save()
            return redirect(show_cart)
        else :
            item.delete()
            return redirect(show_cart)   
        
    else:
        return redirect('home')    
    


def confirm_purchase(request):
    if request.user.is_authenticated:
        items = OrderItem.objects.filter(user=request.user)
        count = items.count()
        transaction_id = uuid.uuid1()
        order_total = 0
        if ShippingAddress.objects.filter(user=request.user,default_address=True).exists():
            delivery_address =ShippingAddress.objects.get(user=request.user,default_address=True)
            for item in items:
                order =Order.objects.create(user = request.user, product=item.product,delivery_address=delivery_address,quantity=item.quantity,transaction_id=transaction_id)
                order.save()
                order_total += item.price
                item.product.quantity = item.product.quantity - item.quantity
                item.product.save()
        
            context = {'count':count,'delivery_address':delivery_address,'order_total':order_total,'items':items,'order_total':order_total}
            return render(request,'confirm_purchase.html',context)
        else:
            return render(request,'confirm_purchase.html')
    else:
        return redirect('home')
    
        
        
        
    #     return redirect(order_history)         
    # else:       
        
    # context = {'delivery_address':delivery_address}
        
        # else:
            # return render(request,'confirm_purchase.html')


        

def order_history(request):
    if request.user.is_authenticated:
        user =request.user
        catagories = Catagory.objects.all()
        orders = Order.objects.filter(user=user,complete=True)
        dict = {}
        for order in orders:
            if not order.transaction_id in dict.keys():
                dict[order.transaction_id]=[]
            dict[order.transaction_id].append(order)
        print(dict)
        context ={'dict':dict,'catagories':catagories}
        return render(request,'user_order_history.html',context)
    else:
        return redirect('home')  

def admin_order_history(request):
    if request.user.is_authenticated:
        
        orders = Order.objects.filter(complete=True)
        dict = {}
        for order in orders:
            if not order.transaction_id in dict.keys():
                dict[order.transaction_id]=[]
            dict[order.transaction_id].append(order)
        print(dict)
        context ={'dict':dict}
        return render(request,'admin_order_history.html',context)
    else:
        return redirect('admin_vendor_page')  

def admin_order_delete(request,id):
    if request.user.is_authenticated:
        orders = Order.objects.filter(transaction_id=id)
        orders.delete()
        return redirect(admin_order_history)
    else:
        return redirect('home')
def vendor_order(request):
    if request.user.is_authenticated:
        orders_all = Order.objects.filter(complete=True)
        print(orders_all)
        orders = []
        for order in orders_all:
            if order.product.vendor == request.user:
                orders.append(order)
        print(orders)
        dict = {}
        for order in orders:
            if not order.transaction_id in dict.keys():
                dict[order.transaction_id]=[]
            dict[order.transaction_id].append(order)
        print(dict)
        context ={'dict':dict}
        return render(request,'vendor_order_history.html',context)
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