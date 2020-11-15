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
        count = items.count()
        return render(request,'user_cart.html',{'items':items,'count':count})
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
                    return redirect(show_cart)
                else:
                    return redirect(show_cart)
            else:
                orderitem = OrderItem.objects.create( user=user, product=product,price=product.price)
                orderitem.save()
                return redirect(show_cart)
        else:
            return redirect(home)

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
            order =Order.objects.create(user = user, product=item.product,quantity=item.quantity, complete=True,transaction_id=transaction_id,)
            order.save()
            order_item = OrderItem.objects.filter(product=item.product)
            order_item.delete()
            ship =ShippingAddress.objects.create(city=city,state=state,pincode=pincode)
            ship.save()
            item.product.quantity = item.product.quantity - item.quantity
            item.product.save()
        return redirect(show_cart)
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
        return render(request,'order_history.html',context)
    else:
        return redirect(home)       