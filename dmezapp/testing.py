from dmezapp.models import Product,Today,Best, newregis, Customer, Order, OrderItem, ShippingAddress
from django.shortcuts import render,redirect
#from django.contrib.auth import authenticate, login
#from django.contrib.auth import logout
from django.contrib.auth.models import User,auth
from django.contrib import messages
t=input('enter')
post=Products.objects.all('desc')
k=post[ ]
print(post)