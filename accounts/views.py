from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings

from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter

def registerPage(request):
	# if request.user.is_authenticated:
	# 	return redirect('home')
	# else:
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + user)

			return redirect('login')
			
	context = {'form':form}
	return render(request, 'accounts/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('index')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('index')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def index(request):
	return render(request, 'accounts/index.html')

# @login_required(login_url='login')
# def marriage(request):
# 	return render(request, 'accounts/marriage.html')

################################################################################################
def childdata(request):
	if request.method == 'POST':
		review_user = request.user
		Cname = request.POST.get('ChildName')
		dob = request.POST.get('DOB')
		Mid = request.POST.get('ParentsMarriageID')

		em = childdata(
			ChildName= Cname, 
			user = review_user, 
			DoB= dob,
			ParentsMarriageID  = Mid
		)
		email1 = EmailMessage(
            "Gewog Management System",
            "Hello " + str(em.user) + " you have successfully added Your Marriage Data in our system. Please wait for few hours, we have to process your details. THANK YOU",
            settings.EMAIL_HOST_USER,
            [review_user.email],)
		email1.fail_silently = False
		email1.send()

		em.save()

		return redirect('index')

	return render(request, 'accounts/childdata.html')
	

		









####################################################################################
@login_required(login_url='login')
def marriage(request):
	if request.method == 'POST':
		review_user = request.user
		# review_query = User.objects.filter(user=review_user)
		# if review_query.exists():
        #     raise ValidationError("You have already reviewed")
		mid = request.POST.get('MarriageId')
		scid = request.POST.get('Spousecid')
		sname = request.POST.get('Spousename')
		marriagecert = request.FILES['MarriageCertificate']
		# POST.get('MarriageCertificate')
		

		em = Marriage(
			MarriageId= mid, 
			user = review_user, 
			Spousecid = scid,
			Spousename = sname,
			MarriageCertificate = marriagecert
		)
		
		email1 = EmailMessage(
            "Gewog Management System",
            "Hello "+ str(em.user) + "you have successfully added Your child Data in our system. Please wait for few hours, we have to process your details. THANK YOU",
            settings.EMAIL_HOST_USER,
            [review_user.email],)
		email1.fail_silently = False
		email1.send()

		em.save()

		return redirect('index')


	return render(request, 'accounts/marriage.html')




###########################################################################################################
            

@login_required(login_url='login')
def personal(request):
	if request.method == 'POST':
		review_user = request.user
		
		# review_query = User.objects.filter(user=review_user)
		# if review_query.exists():
        #     raise ValidationError("You have already reviewed")
		Name = request.POST.get('Name')
		DOB = request.POST.get('DOB')
		Cid = request.POST.get('Cid')
		Chiwog = request.POST.get('Chiwog')
		Village = request.POST.get('Village')
		HouseHoldNo = request.POST.get('HouseholdNumber')
		ThramNo = request.POST.get('ThramNumber')
		upload = request.FILES['ProfilePhoto']
		phone = request.POST.get('phone')
		marriage = request.POST.get('marriage')
		gender = request.POST.get('gender')



		em = UserData( Name=Name, DOB=DOB,
		user = review_user,
		CID=Cid,Chiwog=Chiwog,
		Village=Village, 
		HouseHoldNo= HouseHoldNo, 
		gender=gender,
		ThramNo= ThramNo, 
		profile= upload, 
		contact_number= phone, 
		email = review_user.email)
		# print(em.email)
		# # print(gender)
		# print(em.user)
		email1 = EmailMessage(
            "Gewog Management System",
            "Hello " + em.Name + " you have successfully added Your Data in our system. Please wait for few hours, we have to process your details. THANK YOU",
            settings.EMAIL_HOST_USER,
            [em.email],)
		email1.fail_silently = False
		email1.send()
		em.save()

		if(marriage == 'yes'):
			return redirect('marriage')
		else:
			return redirect('index')


	return render(request, 'accounts/personalinfo.html')




@login_required(login_url='login')
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending }

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def products(request):
	products = Product.objects.all()

	return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
	'myFilter':myFilter}
	return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete.html', context)