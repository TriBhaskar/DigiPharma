from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            
    context = {'form' :form}
    return render(request, 'store/login.html',context)

def home(request):
    context={}
    return render(request, 'store/index.html', context)

def shop(request):
    context={}
    return render(request, 'store/shop.html', context)

def cart(request):
    context={}
    return render(request, 'store/cart.html',context)

def checkout(request):
    context={}
    return render(request, 'store/checkout.html',context)
