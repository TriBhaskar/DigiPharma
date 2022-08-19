from asyncio.windows_events import NULL
import email
from django.db.models import Q
from unicodedata import category
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import datetime

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                password=form.cleaned_data.get('password1')
                user=authenticate(username=username,password=password)
                Customer.objects.create(user=user,name=username,email=email)
                messages.success(request,"Account was created for "+ username)
                return redirect('login')
                
        context = {'form' :form}
        return render(request, 'store/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incoreect')

        context = {}
        return render (request, 'store/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect ('home')

def home(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context={'products' : products, 'items':items, 'order':order}
    return render(request, 'store/index.html', context)

def shop(request):
    q = request.GET.get('q') if request.GET.get('q') !=None else ''
    products =Product.objects.filter(Q(name__icontains=q) | Q(category__name__icontains=q))
    # products = Product.objects.all()
    category=Category.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        category_count = category.count()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    context={'products' : products, 'category':category, 'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/shop.html', context)

@login_required(login_url='login')
def shoppingDetail(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        shipdetail = ShippingAddress.objects.filter(customer = customer)
        # print("this is shipping ",ShippingAddress)
        if not shipdetail:
            return redirect('home')
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        # print("Order is ",order)
        items = order.orderitem_set.all()
        orderafter =Order.objects.filter(customer = customer, complete=True)
        x=orderafter[len(orderafter)-1]
        shipitem = x.orderitem_set.all()
        print("shiipp item :",shipitem)
        # prod = OrderItem.objects.all()
    context ={'items':items,'order':order, 'customer':customer, 'shipdetail':shipdetail[len(shipdetail)-1],'shipitem':shipitem,'x':x}
    return render(request, 'store/shopping_detail.html', context)

# from django.contrib.auth import get_user_model user = get_user_model() user.objects.all()


def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}

    context={'items':items, 'order':order}
    return render(request, 'store/cart.html',context)

@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}

    context={'items':items, 'order':order}
    return render(request, 'store/checkout.html',context)

@login_required(login_url='login')
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer = customer, complete=False)

    orderItem, created =OrderItem.objects.get_or_create(order=order, product=product)

    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action =='remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

@login_required(login_url='login')
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        total =float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                pincode = data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in....')
    return JsonResponse('Payment Complete!', safe=False)