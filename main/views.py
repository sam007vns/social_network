from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth, User
from django.contrib import auth
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from datetime import datetime as reg_date
from django.core.mail import send_mail
from django.conf import settings
from .models import people_data, people_post
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
import magic
import shutil
import math
import random
import json
from django.http import JsonResponse
from simple_search import search_filter
from django.core import serializers

def index(request):
	return render(request,"index.html")
def signup(request):
	if request.method=="POST":
		name=request.POST.get('name','')
		if len(name)<4:
			messages.add_message(request,messages.WARNING,"Please Enter Your Full Name!")
			return redirect('index')
		email=request.POST.get('email','')
		password=request.POST.get('password','')
		if len(password)<8:
			messages.add_message(request,messages.WARNING,"Password should be of 8 characters or greater.")
			return redirect('index')
		month=request.POST.get('month','')
		year=request.POST.get('year','')
		if int(year)>2007 or int(year)<1952:
			messages.add_message(request,messages.WARNING,"Please enter correct details. !")
			return redirect('index')
		username=request.POST.get('username','')
		if len(username)<4:
			messages.add_message(request,messages.WARNING,"Username should be of 4 characters or greater.")
			return redirect('index')
		gender=request.POST.get('gender','')
		if gender!='male':
			if gender != 'female':
				messages.add_message(request,messages.WARNING,"Please enter correct details. !")
				return redirect('index')
		if month=="January":
			month=1
		elif month=="February":
			month=2
		elif month=="March":
			month=3
		elif month=="April":
			month=4
		elif month=="May":
			month=5
		elif month=="June":
			month=6
		elif month=="July":
			month=7
		elif month=="August":
			month=8
		elif month=="September":
			month=9
		elif month=="October":
			month=10
		elif month=="November":
			month=11
		elif month=="December":
			month=12
		else:
			messages.add_message(request,messages.WARNING,"Please Enter correct details")
			return render(request,"index.html")
		day=request.POST.get('day','')
		if type(day)==int:
			if day>31 or day<1:
				messages.add_message(request,messages.WARNING,"Please enter correct details. !")
				return redirect('index')
			if month==2 and day>28:
				messages.add_message(request,messages.WARNING,"Please enter correct details. !")
				return redirect('index')
			if month%2!=0 and month!=2 and day>30:
				messages.add_message(request,messages.WARNING,"Please enter correct details. !")
				return redirect('index')
		d1=datetime.date(int(year),month,int(day))
		date_joined=datetime.datetime.now()
		last_login=datetime.datetime.now()
		if User.objects.filter(email=email).exists():
			messages.add_message(request,messages.WARNING,"Email Already exists")
			return render(request,"index.html")
		elif User.objects.filter(username=username).exists():
			messages.add_message(request,messages.WARNING,"Username Taken")
			return render(request,"index.html")
		else:
			email_verify=list(email)
			email_con=[]
			take=False
			for x in email_verify:
				if x=="@":
					take=True
				if take==True:
					email_con.append(x)
			if len(email_con)<4:
				messages.add_message(request,messages.WARNING,"University Email is required.")
				return render(request,"index.html")
			if "".join(email_con)=="@gla.ac.in":
				user_main = User.objects.create_user(username=username,password=password,email=email,first_name=name)
				user_main.save()
				email_key=random.randint(100000,999999)
				user  =  people_data(username=username, name=name, email=email, password=password,gender=gender,email_key=email_key,last_login=last_login,birth=d1,date_joined=date_joined,status="w")
				user.save()
				mail_info={"name":name,"email_key":email_key}
				html_message = render_to_string('welcome_mail.html', {'info': mail_info})
				plain_message = strip_tags(html_message)
				mail.send_mail('Welcome to GLA-CONNECT', plain_message, 'admin@dineshtutorial.in', [email,], html_message=html_message,fail_silently=True,)
				user = auth.authenticate(username=username, password=password)
				if user:
					auth.login(request,user)
				messages.add_message(request,messages.SUCCESS,"Your account has been registered!. And OTP has been sent to your University email address.")
				return redirect("email_verify")
			else:
				messages.add_message(request,messages.WARNING,"Please Enter University Email !")
				return render(request,"index.html")
def login(request):
	if request.method=="POST":
		username=request.POST.get('username','')
		password=request.POST.get('password','')
		user = auth.authenticate(username=username, password=password)
		if user:
			auth.login(request,user)
			status=people_data.objects.get(username=request.user.username).status
			if status=='w':
				messages.add_message(request,messages.SUCCESS,"Your account has been registered!. And OTP has been sent to your University email address.")
				return redirect('email_verify')
			return redirect(home)
		else:
			messages.add_message(request,messages.WARNING,"Invalid Username or Password")
			return redirect(index)
	else:
		return redirect(index)
@login_required(login_url="index")
def email_verify(request):
	obj=people_data.objects.get(username=request.user.username)
	if request.method=="POST" and request.user.is_authenticated and obj.status=='w':
		otp=request.POST.get('otp','')
		if otp==str(obj.email_key):
			obj.status="Approved"
			obj.save()
			return redirect("home")
		else:
			messages.add_message(request,messages.WARNING,"OTP is not correct!")
			return render(request,"email_verify.html")
	elif request.user.is_authenticated and obj.status=='w':
		return render(request,"email_verify.html")
	else:
		return redirect("index")
@login_required(login_url="index")
def home(request):
	obj=people_data.objects.get(username=request.user.username)
	if obj.status == 'w':
		return redirect('email_verify')
	wall_view=people_post.objects.filter(username=obj.username)
	return render(request,"home.html",{"wall_view":wall_view})
@login_required(login_url="index")
def post_status(request):
	if request.method=="POST":
		obj=people_data.objects.get(username=request.user.username)
		post_data=request.POST.get('post_data','')
		user_post=people_post(username=request.user.username,post_data=post_data)
		user_post.save()
		return HttpResponse("Success!")

	else:
		return redirect('home')

@login_required(login_url="index")
def search(request):
	if request.method=="POST":
		people_search=request.POST.get('people_search','')
		query = people_search
		search_fields = ['name', 'username',]
		f = search_filter(search_fields, query)
		filtered = people_data.objects.filter(f)
		filtered=list(filtered)
		result=[]
		for x in filtered:
			result.append({"name":x.name,"username":x.username})
		# serialized_qs = serializers.serialize('json', result)
		# data = {"queryset" : serialized_qs}
		return HttpResponse(json.dumps(result))
	return render(request,"search.html")
@login_required(login_url="index")
def notifications(request):
	return render(request,"notifications.html")
@login_required(login_url="index")
def chat(request):
	return render(request,"chat.html")