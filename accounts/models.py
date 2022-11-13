from django.db import models
from email.policy import default
from enum import unique
from random import choices
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORY = (
			('Indoor', 'Indoor'),
			('Out Door', 'Out Door'),
			) 

	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name

class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)

	customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	note = models.CharField(max_length=1000, null=True)

	def __str__(self):
		return self.product.name

###################################   my app  ##########################
class UserData(models.Model):
    CID = models.IntegerField(primary_key=True)
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    gen = [
        ('Male', 'Male'),
        ('Female', 'Female')
        ]
    gender = models.CharField(max_length=100, choices = gen)
    DOB = models.DateField()
    profile = models.ImageField(upload_to='image', null= True, blank=True)
    Village = models.CharField(max_length=100)
    Chiwog = models.CharField(max_length=100)
    ThramNo = models.CharField(max_length=100)
    HouseHoldNo = models.CharField(max_length=100)  
    Created = models.DateTimeField(auto_now_add=True)
    contact_number = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    status = models.BooleanField(default=False)


    def __str__(self):
        return str(self.CID)


class Marriage(models.Model):
	MarriageId = models.IntegerField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	Spousecid = models.IntegerField()
	Spousename = models.CharField(max_length=100)
	MarriageCertificate  = models.ImageField(upload_to='image', null=True)
	status = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.Name

class Childdata(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	Child = models.CharField(max_length=100)
	DoB = models.DateField()
	Marriage = models.ForeignKey(Marriage, on_delete=models.CASCADE)

	def __str__(self):
		return self.user + self.Marriage





