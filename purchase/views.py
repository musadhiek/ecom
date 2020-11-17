from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.db import models
from product.models import Product
from .models import OrderItem,Order,ShippingAddress
import uuid

# Create your views here.

def show_cart(request):
    if request.user.is_authenticated:
        user =request.user    
        items = OrderItem.objects.filter(user=user)
        orders = Order.objects.filter(user=user)
        count = items.count()
        total = 0
        for item in items:
            total += item.price
        if count ==0:
            message = "There is no items in Your cart!" 
            return render(request,'user_cart.html',{'items':items,'message':message})
        context ={'items':items,'orders':orders,'count':count,'total':total}    
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
    user = request.user
    if request.user.is_authenticated and request.method=='POST':
        
        # address = request.POST['address']
        city = request.POST['city']   
        state = request.POST['state']
        pincode = request.POST['pincode']
        items = OrderItem.objects.filter(user=user)
        print(items)
        transaction_id = uuid.uuid1()
        for item in items:
            order =Order.objects.create(user = user, product=item.product,quantity=item.quantity,complete=True,transaction_id=transaction_id)
            order.save()
            order_item = OrderItem.objects.filter(product=item.product)
            order_item.delete()
            ship =ShippingAddress.objects.create(city=city,state=state,pincode=pincode)
            ship.save()
            item.product.quantity = item.product.quantity - item.quantity
            item.product.save()
        return redirect(order_history)
    #         return redirect(show_cart)
    #     else:
    #         delivery_address=ShippingAddress.objects.create(user=user,city=city,state=state,pincode=pincode)
    #       
    address= ShippingAddress.objects.filter(user=user)
    return render(request,'confirm_purchase.html',{'address':address})

def order_history(request):
    if request.user.is_authenticated:
        user =request.user
        orders = Order.objects.filter(user=user,complete=True)
        dict = {}
        for order in orders:
            if not order.transaction_id in dict.keys():
                dict[order.transaction_id]=[]
            dict[order.transaction_id].append(order)
        print(dict)
        context ={'dict':dict}
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