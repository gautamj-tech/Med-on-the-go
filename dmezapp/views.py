from django.shortcuts import render,redirect
#from django.contrib.auth import authenticate, login
#from django.contrib.auth import logout
from django.contrib.auth.models import User,auth
from django.contrib import messages
from dmezapp.models import Product,Covid,Today,Best, newregis, Customer, Order, OrderItem, ShippingAddress, Single
from math import ceil
from django.http import JsonResponse
import datetime
from .utils import cookieCart, cartData, guestOrder
import json
from dmezapp.chatbot import chatbot
import os
import smtplib
from django.core.mail import send_mail

# Create your views here.
def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.name.lower() or query in item.category.lower():
        return True
    else:
        return False
def search(request):
	search = request.GET.get('search')
	allProds = []
	catprods = Product.objects.values('category', 'id')
	cats = {item['category'] for item in catprods}
	for cat in cats:
		prodtemp = Product.objects.filter(category=cat)
		prod = [item for item in prodtemp if searchMatch(search, item)]
		n = len(prod)
		nSlides = n // 4 + ceil((n / 4) - (n // 4))
		if len(prod) != 0:
			allProds.append([prod, range(1, nSlides), nSlides])
	params = {'allProds': allProds, "msg": ""}
	if len(allProds) == 0 or len(search) < 4:
		params = {'msg': "Please make sure to enter relevant search query"}
		return render(request, 'notfound.html', params)
	return render(request, 'search.html', params)



def home(request):
	products= Product.objects.all()
	Todays= Today.objects.all()
	covids= Covid.objects.all()
	Bests= Best.objects.all()
	context= {'Todays':Todays,'products':products,'covids':covids,'Bests':Bests}
	return render(request,'index.html',context)
#contact us....................
def coming(request):
	if request.method =="POST":
		to = request.POST.get('email')
		content=request.POST.get('message')
		name=request.POST.get('name')
		number=request.POST.get('number')
		customer="Dear "+ name + "!!\nWe will contact you soon.."
		dmez='This mail from:'+ name +"..\nmob number:"+ number +"\nemail id:"+ to + "\nmessage:"+ content
		print(to,content)
		send_mail(
		"Hello",customer,'customersupport@dmez.in',[to])
		send_mail(
		"testing",dmez,settings.EMAIL_HOST_USER,['customersupport@dmez.in','anjuvigil212@gmail.com'])
		return render(request,'index.html',{'title':'send an email'})

	else:
 	   return render(request,'coming.html',{'title':'send an email'})
#..............................
def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'allproduct.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'cart.html', context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def checkout(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'checkout.html', context)



def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)


def ayurvedhic(request):

	return render(request,'ayurvedhic.html')




def allproduct(request):
    allProds = []
    catprods = Products.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Products.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'allproduct.html', params)

def productView(request, myid):

    # Fetch the product using the id
    products = Product.objects.filter(id=myid)

    return render(request, 'product.html', {'products':products[0]})
def todayView(request, myid):

    # Fetch the product using the id

    Todays = Today.objects.filter(id=myid)
    return render(request,'today.html',  {'Todays':Todays[0]})

def bestView(request, myid):

    # Fetch the product using the id

    Bests = Best.objects.filter(id=myid)
    return render(request,'best.html',  {'Bests':Bests[0]})
def covid(request, myid):
	covids = Covid.objects.filter(id=myid)
	return render(request,'covid.html', {'covids':covids[0]})

def about(request):
	return render(request,'about.html')

def contact(request):
	return render(request,'contact.html')

def testing(request):
	return render(request,'testing.html')

def join(request):
	return render(request,'join.html')

def upload(request):
	return render(request,'upload.html')

def top(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	singles = Single.objects.all()
	context = {'singles':singles, 'cartItems':cartItems}
	return render(request,'top.html', context)

def specific(request, myid):
    # Fetch the product using the id
    singles = Single.objects.filter(id=myid)
    return render(request, 'specificpage.html', {'singles':singles[0]})


def bestselling(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request,'bestsellingproduct.html', context)


def account(request):
	return render(request,'account.html')

def consult(request):
	return render(request,'consult.html')

def tracker(request):
	return render(request, 'tracker.html')




########################Account Section#############################

def signup(request):
	if request.method=='POST':
		username = request.POST['username']
		email = request.POST['email']
		password1 = request.POST['password1']
		password11 = request.POST['password11']
		if password1==password11:
			if User.objects.filter(username=username).exists():
				messages.info(request,'Username Taken')
				return redirect('/account')
			elif User.objects.filter(email=email).exists():
				messages.info(request,'Email Taken')
				return redirect('/account')
			else:
				user=User.objects.create_user(username=username, password=password1, email=email)
				user.save();
				auth.login(request,user)
				print('user created')
				Customer.objects.create(user=user, name=username, email=user.email)
		else:
			messages.info(request,'Password not Matching')
			return redirect('/account')
		return redirect('/')


	else:
		return render(request,'account.html')


def login(request):
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']
		user=auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request,user)
			return redirect('/')
		else:
			return redirect('/account')
	else:
		return render(request,'account.html')

def logout(request):
	auth.logout(request)
	return redirect('/')
def bot(request):
    return render(request,"chatbot.html")
def get_bot_response(request):
    query = request.GET.get('query')
    ans=str(chatbot.get_response(query))
    return render(request, 'chatbot.html', {'ans': ans, 'query': query})
def customerservice(request):
    return render(request,"contacts.html")
def email(request):

    message = request.GET.get('message')
    name = request.GET.get('name')
    phone = request.GET.get('phone')
    email = request.GET.get('email')
    recieved = "Thank you " + name + "!!\nWe have Recieved Your Query.."
    data='from : '+name+',\nphone number : '+phone+',\nemail id : '+email+',\nMessage : '+message
    if len(message)!=0:
        send_mail('Query!!', data, 'dmezservice@gmail.com', ['customersupport@dmez.in'], fail_silently=False)
        return render(request,"contacts.html",{'recieved':recieved})
    else:
        recieved = "No message entered!!!"
        return render(request,"contacts.html",{'recieved':recieved})


def wallet(request):
    return render(request,"wallet.html")
